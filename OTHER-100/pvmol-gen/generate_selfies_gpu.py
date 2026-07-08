"""Single-GPU SELFIES generation worker. Launched as separate process per GPU."""

import argparse
import os
import time

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem, RDLogger
import selfies as sf

RDLogger.DisableLog("rdApp.*")


def validate_smiles(smi):
    try:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            return None
        return Chem.MolToSmiles(mol, canonical=True)
    except:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--known-file", type=str, required=True)
    parser.add_argument("--output-file", type=str, required=True)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--max-length", type=int, default=128)
    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)
    device = torch.device("cuda:0")

    print(f"[GPU {args.gpu}] Loading SELFIES model from {args.model_path}", flush=True)
    tokenizer = GPT2Tokenizer.from_pretrained(args.model_path)
    model = GPT2LMHeadModel.from_pretrained(args.model_path).to(device)
    model.eval()

    with open(args.known_file, "r") as f:
        known = set(line.strip() for line in f if line.strip())
    print(f"[GPU {args.gpu}] Known SMILES: {len(known)}", flush=True)

    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(device)

    generated = {}  # canonical SMILES -> True
    attempts = 0
    valid_selfies = 0
    valid_smiles = 0
    t0 = time.time()
    last_report = t0

    while len(generated) < args.target and attempts < args.target * 5000:
        try:
            batch_input = input_ids.repeat(args.batch_size, 1)
            attention_mask = torch.ones_like(batch_input)

            with torch.no_grad():
                outputs = model.generate(
                    batch_input,
                    attention_mask=attention_mask,
                    max_length=args.max_length,
                    num_return_sequences=args.batch_size,
                    temperature=args.temperature,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                )

            for seq in outputs:
                raw = tokenizer.decode(seq, skip_special_tokens=True).strip()
                attempts += 1

                # Decode SELFIES → SMILES
                try:
                    smi = sf.decoder(raw)
                    if smi:
                        valid_selfies += 1
                        canon = validate_smiles(smi)
                        if canon:
                            valid_smiles += 1
                            if canon not in generated and canon not in known:
                                generated[canon] = True
                except:
                    pass

        except Exception as e:
            print(f"[GPU {args.gpu}] Error: {e}", flush=True)
            attempts += args.batch_size

        now = time.time()
        if now - last_report > 30:
            elapsed = now - t0
            rate = len(generated) / elapsed if elapsed > 0 else 0
            sf_rate = valid_selfies / max(attempts, 1) * 100
            smi_rate = valid_smiles / max(attempts, 1) * 100
            eta = (args.target - len(generated)) / rate / 60 if rate > 0 else 999
            print(f"[GPU {args.gpu}] {len(generated)}/{args.target} CUN "
                  f"(SELFIES valid: {sf_rate:.1f}%, SMILES valid: {smi_rate:.1f}%, "
                  f"{rate:.1f}/s, ETA {eta:.0f}min)", flush=True)
            last_report = now

    elapsed = time.time() - t0
    print(f"[GPU {args.gpu}] DONE: {len(generated)} CUN molecules in {elapsed/60:.1f} min "
          f"(SELFIES valid: {valid_selfies/max(attempts,1)*100:.1f}%, "
          f"SMILES valid: {valid_smiles/max(attempts,1)*100:.1f}%)", flush=True)

    with open(args.output_file, "w") as f:
        for smi in generated:
            f.write(smi + "\n")


if __name__ == "__main__":
    main()
