"""条件算术，不验证输入证据。所有时间须同边界串行可加。"""
import argparse
import json
import math

def finite(x):
    if isinstance(x, bool) or not isinstance(x,(int,float)) or not math.isfinite(x):
        raise ValueError('需要有限数值')
    return x

def analyze(stage, share, target, unaffected_case_share=None):
    for x in (stage,share,target): finite(x)
    if stage<=0 or not 0<share<=1 or target<0: raise ValueError('时间/占比不合法')
    total=stage/share
    other=total-stage
    remaining=target-other
    r=dict(status='conditional_inference_not_observation',baseline_total=total,unchanged_other=other,allowed_stage=remaining,required_stage_reduction=(stage-remaining)/stage,total_reduction=(total-target)/total,target_feasible_by_stage_alone=remaining>=0,assumptions=['同一边界串行可加','分钟和占比口径一致','其他环节不变'])
    if unaffected_case_share is not None:
        u=finite(unaffected_case_share)
        if not 0<=u<=1: raise ValueError('不改善案件比例必须在[0,1]，不能直接使用单据比例')
        r['whole_population_floor']=other+u*stage
        r['target_feasible_with_coverage']=target>=r['whole_population_floor']
        r['assumptions']+=['比例为案件而非单据','各组原始基线相同','该组核对完全不改善']
    return r

def weighted_time(other,stage,u,improved):
    for x in (other,stage,u,improved): finite(x)
    if min(other,stage,improved)<0 or not 0<=u<=1: raise ValueError('时间或比例不合法')
    return other+u*stage+(1-u)*improved

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('stage','share','target'): p.add_argument('--'+arg,type=float,required=True)
    p.add_argument('--unaffected-case-share',type=float)
    a=p.parse_args()
    try: r=analyze(a.stage,a.share,a.target,a.unaffected_case_share)
    except ValueError as e: p.error(str(e))
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False))
if __name__=='__main__': main()
