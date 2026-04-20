"""Single-GPU generation worker. Launched as a separate process per GPU."""

import argparse
import os
import time

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem, RDLogger

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
    parser.add_argument("--batch-size", type=int, default=48)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--max-length", type=int, default=100)
    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)
    device = torch.device("cuda:0")

    print(f"[GPU {args.gpu}] Loading model from {args.model_path}", flush=True)
    tokenizer = GPT2Tokenizer.from_pretrained(args.model_path)
    model = GPT2LMHeadModel.from_pretrained(args.model_path).to(device)
    model.eval()

    # Load known SMILES
    with open(args.known_file, "r") as f:
        known = set(line.strip() for line in f if line.strip())
    print(f"[GPU {args.gpu}] Known SMILES: {len(known)}", flush=True)

    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(device)

    generated = set()
    attempts = 0
    max_attempts = args.target * 50000  # 0.3% valid rate needs ~33K attempts per mol
    t0 = time.time()
    last_report = t0

    while len(generated) < args.target and attempts < max_attempts:
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
                smiles = tokenizer.decode(seq, skip_special_tokens=True).strip()
                canon = validate_smiles(smiles)
                if canon and canon not in generated and canon not in known:
                    generated.add(canon)
                attempts += args.batch_size

        except Exception as e:
            print(f"[GPU {args.gpu}] Error: {e}", flush=True)
            attempts += args.batch_size

        now = time.time()
        if now - last_report > 30:
            elapsed = now - t0
            rate = len(generated) / elapsed if elapsed > 0 else 0
            valid_pct = len(generated) / max(attempts, 1) * 100
            eta = (args.target - len(generated)) / rate / 60 if rate > 0 else 999
            print(f"[GPU {args.gpu}] {len(generated)}/{args.target} "
                  f"({valid_pct:.1f}% valid, {rate:.1f}/s, ETA {eta:.0f}min)",
                  flush=True)
            last_report = now

    elapsed = time.time() - t0
    print(f"[GPU {args.gpu}] DONE: {len(generated)} molecules in {elapsed/60:.1f} min",
          flush=True)

    with open(args.output_file, "w") as f:
        for smi in generated:
            f.write(smi + "\n")


if __name__ == "__main__":
    main()
