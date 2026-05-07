#!/usr/bin/env python3
"""
Master script to run all PINN-RANS test cases.
Run on uicgpu for GPU acceleration.

Usage:
    python run_all.py [--cases fsbl,zpg,hill] [--quick]
"""

import sys
import os
import json
import time
import argparse

sys.path.insert(0, os.path.dirname(__file__))


def run_fsbl():
    """Run Falkner-Skan boundary layer case."""
    from train_fsbl import main as train_fsbl
    return train_fsbl()


def run_zpg():
    """Run ZPG turbulent boundary layer case."""
    from train_zpg import main as train_zpg
    return train_zpg()


def run_hill():
    """Run periodic hill case."""
    from train_periodic_hill import main as train_hill
    return train_hill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cases', default='fsbl,zpg,hill',
                       help='Comma-separated list of cases to run')
    parser.add_argument('--quick', action='store_true',
                       help='Quick mode: fewer epochs for testing')
    args = parser.parse_args()
    
    cases = args.cases.split(',')
    
    all_results = {}
    t_start = time.time()
    
    for case in cases:
        case = case.strip()
        print(f"\n{'='*70}")
        print(f"Running case: {case}")
        print(f"{'='*70}\n")
        
        try:
            if case == 'fsbl':
                result = run_fsbl()
            elif case == 'zpg':
                result = run_zpg()
            elif case == 'hill':
                result = run_hill()
            else:
                print(f"Unknown case: {case}")
                continue
            
            all_results[case] = result
            print(f"\n✓ {case} completed successfully")
            
        except Exception as e:
            print(f"\n✗ {case} failed: {e}")
            import traceback
            traceback.print_exc()
            all_results[case] = {'error': str(e)}
    
    t_total = time.time() - t_start
    
    # Summary
    print(f"\n{'='*70}")
    print(f"ALL CASES COMPLETE — Total time: {t_total:.1f}s")
    print(f"{'='*70}")
    
    for case, result in all_results.items():
        if 'error' in result:
            print(f"  {case}: FAILED — {result['error']}")
        else:
            errs = result.get('errors', {})
            err_str = ', '.join(f"{k}={v:.2f}%" for k, v in errs.items())
            print(f"  {case}: {err_str}")
    
    # Save combined results
    outdir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(outdir, 'all_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\nAll results saved to {outdir}/all_results.json")
    return all_results


if __name__ == '__main__':
    main()
