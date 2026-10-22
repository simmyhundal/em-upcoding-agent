"""Exploratory event study: payer share prices around earnings releases, and the "cynic's hypothesis".

First pass, free data only. Two stages, so that untrusted downloaded files are read only by a stdlib script run with -I:
  python3 -I eval/payer_event_study.py extract --data DIR --out EXTRACT.csv
      reads the earnings-release HTML (EX-99.1), the SEC submissions JSON and the 8-K list in DIR, pulls the quarter's
      medical-loss-ratio type ratio (this quarter and year-ago), adjusted EPS (this quarter and year-ago), full-year
      adjusted EPS guidance and the acceptance time, and writes one row per 8-K Item 2.02 filing.
  python3 eval/payer_event_study.py analyze --data DIR --extract EXTRACT.csv --out experiments/payer_event_study.csv --report REPORT.txt
      needs numpy; reads the extract and the Yahoo price JSON, builds abnormal returns, runs the regressions and the
      exploratory "cynic" tests, writes the per-event CSV and prints tables for docs/market_event_study_mlr.md.
Method, limits and results: docs/market_event_study_mlr.md. Nothing here uses the synthetic claims data or the answer keys."""
import re, json, glob, os, sys, csv, html, datetime, math, random
def to_text(raw):
    s=re.sub(r'(?is)<(script|style).*?</\1>','',raw)
    s=re.sub(r'(?i)</(td|th)>',' | ',s)
    s=re.sub(r'(?i)</(tr|p|div|br|li|h\d)>|<br\s*/?>','\n',s)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s).replace('\xa0',' ')
    return s
def flat(s): return re.sub(r'\s+',' ',s)
PCT=r'(\d{2}(?:\.\d{1,2})?)\s*(?:%|percent)'
def pct_after(s,start,n=1,span=400):
    w=s[start:start+span]
    return [float(x) for x in re.findall(PCT,w)][:n]

def prep(path):
    s=flat(to_text(open(path,errors='ignore').read()))
    s=re.sub(r'\s*\.{4,}\s*',' | ',s)
    s=re.sub(r'(?:\|\s*)+','| ',s)
    return s
def body(s):
    i=s.find('-->')
    return s[i:] if 0<i<6000 else s
def nums_after(s,label_re,k=4,span=170,flags=re.I,which=0):
    rows=[]
    for m in re.finditer(label_re,s,flags):
        w=s[m.end():m.end()+span]
        toks=re.findall(r'\(?\$?\s?-?\d[\d,]*\.?\d*\)?|[A-Za-z]{4,}',w)
        vals=[]
        for t in toks:
            if re.match(r'[A-Za-z]',t):
                if vals: break
                continue
            neg=t.startswith('(')
            v=re.sub(r'[()$\s,]','',t)
            try: x=float(v)
            except: continue
            vals.append(-x if neg else x)
        rows.append(vals[:k])
    return rows
def ok(v,lo=60,hi=105): return v is not None and lo<=v<=hi

# ---------- MLR pair from narrative -------------
BPS=r'(\d{1,4})[\s-]*(?:basis|bps|bp\b)'
def narrative_pair(s,name_re,qword=True):
    """return (cur,prior,method) from narrative sentences"""
    for m in re.finditer(name_re,s,re.I):
        pre=s[max(0,m.start()-90):m.start()]
        w=s[m.start():m.start()+330]
        head=w[:140]
        # skip full-year-only mentions
        if re.search(r'full[- ]year|year ended|for 20\d\d and',pre[-60:]+head[:90],re.I) and not re.search(r'quarter',pre[-60:]+head[:110],re.I):
            continue
        p=re.search(PCT,w)
        if not p: continue
        cur=float(p.group(1))
        # prior via compared/from
        q=re.search(r'(?:compared (?:to|with)|compares to|from|versus|vs\.?|relative to|up from|down from|over)\s+(?:a |an |the )?(?:\w+\s){0,3}?'+PCT,w[p.end():p.end()+250],re.I)
        # ensure the compared figure is a pct reached before another sentence
        if q:
            pr=float(q.group(1))
            return cur,pr,'nar'
        b=re.search(BPS,w[p.end():p.end()+160],re.I)
        if b:
            seg=w[p.end():p.end()+b.end()+p.end()]
            d=re.search(r'(increase|increased|higher|up|rise|rose|deterior\w+)|(decrease|decreased|decline\w*|improve\w*|lower|down|reduc\w+|favorable)',w[p.end():p.end()+160],re.I)
            if d and not re.search(r'adjust',w[p.end():p.end()+160][:60],re.I):
                sign=1 if d.group(1) else -1
                return cur,round(cur-sign*float(b.group(1))/100,2),'bps'
    return None

# ================= per company ==================
def first_row(s,label_re,minn=2,pred=None,k=6,span=170):
    for r in nums_after(s,label_re,k=k,span=span):
        if len(r)>=minn and (pred is None or pred(r)): return r
    return None

def mlr(t,s,res):
    """return dict(cur,prior,method) or None; res = narrative+table candidates"""
    out={}
    if t=='UNH':
        prem=first_row(s,r'\bPremiums\s*\|',2,lambda r:r[0]>5000 and r[1]>5000)
        cost=first_row(s,r'\bMedical costs\s*\|',2,lambda r:r[0]>5000 and r[1]>5000)
        tab=None
        if prem and cost: tab=(round(100*cost[0]/prem[0],2),round(100*cost[1]/prem[1],2))
        nar=narrative_pair(s,r'medical care ratio')
        out['tab']=tab; out['nar']=nar
    elif t=='ELV':
        r=first_row(s,r'Benefit expense as a percentage of premiums\s*\|',2,lambda r:60<r[0]<100 and 60<r[1]<100)
        out['tab']=(r[0],r[1]) if r else None
        out['nar']=narrative_pair(s,r'benefit expense ratio')
    elif t=='CNC':
        out['nar']=narrative_pair(s,r'(?:health benefits ratio|HBR)')
        r=first_row(s,r'\bHBR\s*\|',2,lambda r:60<r[0]<110 and 60<r[1]<110 and abs(r[0]-r[1])<10 and r[1]!=r[0] or True)
        out['tab']=None
    elif t=='CI':
        out['nar']=narrative_pair(s,r'(?:Cigna Healthcare )?(?:medical care ratio|MCR)(?: \d(?:,\d)*)?')
        out['tab']=None
    elif t=='CVS':
        r=first_row(s,r'Medical benefit ratio \(“MBR”\) \(\d\)\s*\|',2,lambda r:60<r[0]<110 and 60<r[1]<110)
        out['tab']=(r[0],r[1]) if r else None; out['nar']=None
    elif t=='HUM':
        mm=re.search(r'INSURANCE SEGMENT\s*Benefit ratio',s)
        i=s.find('INSURANCE SEGMENT')
        lab=r'Benefit(?:s)?(?: expense)? ratio\s*(?:[–-]\s*GAAP)?\s*\|'
        pr=lambda r:60<r[0]<110 and 60<r[1]<110
        r=None
        if mm: r=first_row(s[mm.end():mm.end()+400],r'\bGAAP\s*\|',2,pr)
        if r is None: r=first_row(s[i:],lab,2,pr) if i>0 else first_row(s,lab,2,pr)
        if r is None:
            j=s.find('Insurance Segment Benefit Ratio')
            if j>0: r=first_row(s[j:],r'\bGAAP\s*\|',2,pr)
        out['tab']=(r[0],r[1]) if r else None; out['nar']=None
    return out

def eps(t,s):
    pr=lambda r:abs(r[0])<80 and abs(r[1])<80
    r=None
    if t=='UNH':
        for lab in [r'Adjusted earnings per share attributable to UnitedHealth Group common shareholders(?:\s*\(\w\))*\s*\|',r'Adjusted net earnings per share attributable to UnitedHealth Group common shareholders(?:\s*\(\w\))*\s*\|',r'Adjusted diluted earnings per share\s*\|',r'Adjusted net earnings per share\s*\|']:
            r=first_row(s,lab,2,pr)
            if r: break
    elif t=='ELV':
        for lab in [r'Adjusted (?:shareholders[’\']? )?(?:net income|earnings) per diluted share\s*\|\s*\$\s*\|',r'Adjusted (?:shareholders[’\']? )?(?:net income|earnings) per diluted share\s*\|(?!\s*(?:Greater|Approx|At least))',r'Adjusted net income per share\s*\|',r'Adjusted diluted EPS\s*\|']:
            r=first_row(s,lab,2,pr)
            if r: break
    elif t=='CI':
        r=first_row(s,r'Adjusted Income from Operations[\d, ]*,? per share\s*\|',2,pr) or first_row(s,r'Adjusted income from operations(?: \(\d\))?\s*\|\s*\$\s*\|\s*[\d.]+\s*\|\s*\$',2,pr)
    elif t=='CVS':
        r=first_row(s,r'Adjusted EPS(?: \(\d\))?\s*\|',2,pr)
    elif t=='HUM':
        r=first_row(s,r'EPS\s*[-–]\s*Adjusted(?: \(non-GAAP\))?\s*\|',2,pr)
        if not r:
            j=s.find('Diluted earnings per share (EPS)')
            if j>0: r=first_row(s[j:j+900],r'Adjusted \(non-GAAP\)\s*\|',2,pr)
        if not r:
            for hm in re.finditer(r'per share[^|]{0,40}\|\s*[1-4]Q\d\d',s,re.I):
                r=first_row(s[hm.end():hm.end()+500],r'Adjusted \(non-GAAP\)\s*\|',2,pr)
                if r: break
    elif t=='CNC':
        lab=r'Adjusted diluted (?:EPS|earnings(?: \(loss\))? per share)\s*\|'
        r=first_row(s,lab,2,pr,span=200)
    return (r[0],r[1]) if r else None

D_=r'\$?\s?(\d{1,3}(?:\.\d{1,2})?)'
RNG=r'(?:\s*(?:to|-|–|—|and)\s*\$?\s?(\d{1,3}(?:\.\d{1,2})?))?'
def _mk(m,fg=1):
    q=(m.group(1) or '').lower() if m.re.groups>=3 else ''
    return q
def guid_eps(t,s):
    """full-year adjusted EPS guidance -> (lo,hi,form) ; form in range/point/floor"""
    cands=[]
    def add(lo,hi,qual,pos):
        lo=float(lo); hi=float(hi) if hi else None
        q=(qual or '').lower()
        if hi and hi>lo and hi<lo*1.5: cands.append((pos,lo,hi,'range'))
        elif re.search(r'at least|greater|more than|above|floor|minimum',q): cands.append((pos,lo,lo,'floor'))
        else: cands.append((pos,lo,lo,'point'))
    if t=='UNH':
        for m in re.finditer(r'adjusted (?:net )?(?:earnings|EPS)(?: per share)?(?: outlook)?(?: of| to| is| range of)?(?: a range of)?\s*(at least|greater than|more than)?\s*'+D_+RNG+r'(?:\s*per share)?',s,re.I):
            ctx=s[max(0,m.start()-260):m.end()+30]
            if re.search(r'outlook|guidance',ctx,re.I) and not re.search(r'(fourth|first|second|third) quarter[^.]{0,60}$',s[max(0,m.start()-60):m.start()],re.I):
                add(m.group(2),m.group(3),m.group(1),m.start())
        for m in re.finditer(r'Adjusted diluted earnings per share\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*(at least |greater than )?\$?(\d+\.\d\d)(?:\s*[-–]\s*\$?(\d+\.\d\d))?',s,re.I):
            add(m.group(2),m.group(3),m.group(1),m.start())
    elif t=='ELV':
        for m in re.finditer(r'Adjusted (?:shareholders[’\']? )?(?:net income|earnings) per diluted share\s*\|\s*(Greater than|Approximately|At least)\s*\|?\s*\$?\s*\|?\s*(\d{2}\.\d\d)()',s,re.I):
            add(m.group(2),None,m.group(1),m.start())
        if not cands:
            for m in re.finditer(r'adjusted net income[^$.]{0,60}?(?:expected )?to be\s*(greater than|approximately|at least)?\s*\$\s?(\d{2}\.\d\d)',s,re.I):
                add(m.group(2),None,m.group(1),m.start())
        if not cands:
            for m in re.finditer(r'adjusted diluted EPS[^$]{0,60}?guidance of\s*(greater than|approximately|at least)?\s*\$\s?(\d{2}\.\d\d)',s,re.I):
                add(m.group(2),None,m.group(1),m.start())
    elif t=='CI':
        for m in re.finditer(r'(at least|in the range of|approximately|~)\s*\$\s?(\d{2}\.\d\d)(?:\s*(?:to|-|–)\s*\$\s?(\d{2}\.\d\d))?\s*per share',s,re.I):
            ctx=s[max(0,m.start()-230):m.start()]
            if re.search(r'adjusted income from operations',ctx,re.I) and not re.search(r'(?:first|second|third|fourth) quarter[^.]{0,40}was',ctx[-140:],re.I):
                add(m.group(2),m.group(3),m.group(1),m.start())
        for m in re.finditer(r'(?:or|,)\s*\$\s?(\d{2}\.\d\d)\s*(?:to|-|–)\s*\$\s?(\d{2}\.\d\d)\s*per share',s,re.I):
            ctx=s[max(0,m.start()-260):m.start()]
            if re.search(r'adjusted income from operations',ctx,re.I) and re.search(r'projected|outlook|expected',ctx,re.I):
                add(m.group(1),m.group(2),'',m.start())
    elif t=='CVS':
        for m in re.finditer(r'Adjusted EPS(?: \(\d\))?\s*(?:guidance)?[^$]{0,50}?(at least)?\s*\$(\d+\.\d\d)(?:\s*(?:to|-|–)\s*\$(\d+\.\d\d))?',s,re.I):
            ctx=s[m.start():m.start()+110]
            if re.search(r'guidance|range|expected',ctx[:100],re.I) and not re.search(r'Adjusted EPS(?: \(\d\))? (?:of|was)',ctx[:30],re.I) and m.start()>0:
                add(m.group(2),m.group(3),m.group(1) or ('at least' if re.search(r'at least',ctx[:60],re.I) else ''),m.start())
    elif t=='HUM':
        for m in re.finditer(r'Adjusted EPS(?: guidance)?(?: of| to| range of|, now)?(?: in a range of| a range of)?\s*[\'"“‘]?\s*(at least|approximately|about)?\s*\$\s?(\d+\.\d\d)(?:\s*(?:to|-|–)\s*\$\s?(\d+\.\d\d))?',s,re.I):
            ctx=s[max(0,m.start()-100):m.end()+60]
            if re.search(r'guidance|FY|full year|affirm|reaffirm|revise|expect',ctx,re.I) and not re.search(r'Adjusted EPS of \$[\d.]+;|Adjusted EPS of \$[\d.]+ on',s[m.start():m.end()+3]):
                add(m.group(2),m.group(3),m.group(1),m.start())
    elif t=='CNC':
        for m in re.finditer(r'adjusted diluted (?:EPS|earnings per share)[^$]{0,110}?(at least|greater than|floor of greater than|of greater than)?\s*\$\s?(\d{1,2}\.\d\d)(?:\s*(?:to|-|–)\s*\$\s?(\d{1,2}\.\d\d))?',s,re.I):
            ctx=s[max(0,m.start()-120):m.end()+30]
            if re.search(r'guidance|outlook|annual',ctx,re.I):
                add(m.group(2),m.group(3),m.group(1) or ('floor' if re.search(r'floor|greater than|at least',s[m.start():m.end()],re.I) else ''),m.start())
        for m in re.finditer(r'adjusted diluted EPS (?:forecast|guidance)[^$]{0,60}?to\s*(at least)?\s*\$\s?(\d{1,2}\.\d\d)()',s,re.I):
            add(m.group(2),None,m.group(1) or 'at least',m.start())
        for m in re.finditer(r'Adjusted diluted EPS\s*\|[^A-Za-z]{0,120}?(at least|greater than)?\s*\$\s?(\d{1,2}\.\d\d)(?:\s*[-–]\s*\$\s?(\d{1,2}\.\d\d))?\s*\|\s*\(\d\)',s,re.I):
            add(m.group(2),m.group(3),m.group(1),m.start())
    if t=='HUM':
        for m in re.finditer(r'(at least|approximately|about)?\s*\$\s?(\d{1,2}\.\d\d)(?:\s*(?:to|-|–)\s*\$\s?(\d{1,2}\.\d\d))?[\'’]?\s+on (?:an )?Adjusted basis',s,re.I):
            ctx=s[max(0,m.start()-170):m.start()]
            if re.search(r'guidance|expect',ctx,re.I) and not re.search(r'reports?\b|reporting|(?:FY|full year) 20\d\d (?:earnings per share|EPS)\s*(?:\(EPS\)\s*)?of\s*\$[\d.]+ on a GAAP',ctx[-75:],re.I):
                add(m.group(2),m.group(3),m.group(1),m.start())
    return cands

def pick_guid(c,t=None):
    if not c: return None
    if t=='CNC':
        r=[x for x in c if x[3]=='range']
        if r: c=r
        else:
            f=[x for x in c if x[3]=='floor']
            if f: c=f
    # annual guidance is the largest EPS-like number among candidates (quarterly EPS candidates are smaller)
    best=max(c,key=lambda x:(x[1],x[0]))
    # if several with same value fine
    return best[1],best[2],best[3]

def mlr_guid(t,s):
    """full-year guided MLR midpoint, only from explicit guidance wording (not validated beyond a 10-event spot check)"""
    N=r'(\d{2}(?:\.\d{1,2})?)'
    lead=r'(?:is |are )?(?:now )?(?:expected|projected|forecast|guidance(?: range)?(?: of)?|outlook(?: of)?)(?: to be)?(?: in the range of| between| of)?\s*(?:approximately |about )?'
    name=r'(?:medical care ratio|benefit expense ratio|benefit ratio|medical benefit ratio|MCR|health benefits ratio|HBR)'
    pats=[name+r'[\s\d,]*[^|%$.]{0,30}?'+lead+N+r'\s*(?:%|percent)(?:\s*(?:to|-|–|and)\s*'+N+r'\s*(?:%|percent))?',
          r'Medical Care Ratio[\s\d,]*\|\s*'+N+r'%\s*to\s*()'+N+r'%',
          name+r'[^%]{0,45}?'+N+r'\s*%\s*\+/-',
          name+r'\s*guidance[^%]{0,30}?'+N+r'\s*percent,? plus or minus']
    for k,pat in enumerate(pats):
        for m in re.finditer(pat,s,re.I):
            span=s[m.start():m.end()]
            if re.search(r'\bfrom\b|increas|decreas|compar|quarter|three months',span,re.I): continue
            ctx=s[max(0,m.start()-250):m.end()+50]
            if k in (0,2) and not re.search(r'guidance|outlook|expect|20\d\d',ctx,re.I): continue
            g=[x for x in m.groups() if x not in (None,'')]
            v=[float(x) for x in g if re.match(r'^\d',x)]
            if v and all(70<x<100 for x in v): return sum(v[:2])/len(v[:2]) if len(v)>1 else v[0]
    return None

QN={'first':1,'second':2,'third':3,'fourth':4}
def ci_quarter_vals(s):
    d={}
    Q=r'(first|second|third|fourth) quarter,? (?:of )?(20\d\d)'
    for m in re.finditer(r'(?:MCR|medical care ratio)[\s\d,]*(?:\(“MCR”\))?\s*(?:of|was|were)\s*(\d\d\.\d)\s*%\s*(?:and \d\d\.\d\s*%\s*)?for\s*(?:the )?'+Q,s,re.I):
        d.setdefault((QN[m.group(2).lower()],int(m.group(3))),float(m.group(1)))
    for m in re.finditer(r'(?:compares? to|compared to|relative to|from)\s*(?:a |an |the )?(?:\w+ ){0,3}?(\d\d\.\d)\s*%\s*for\s*(?:the )?'+Q,s,re.I):
        d.setdefault((QN[m.group(2).lower()],int(m.group(3))),float(m.group(1)))
    for m in re.finditer(Q+r'\s*(?:Cigna Healthcare )?(?:MCR|medical care ratio)[\s\d,]*(?:of|was)\s*(\d\d\.\d)\s*%',s,re.I):
        d.setdefault((QN[m.group(1).lower()],int(m.group(2))),float(m.group(3)))
    return d


def hum_narr(s):
    out={}
    m=re.search(r'\dQ\d\d Insurance segment (?:GAAP |Adjusted )?benefit ratio of (\d\d\.\d) percent',s,re.I)
    if m: out['mlr_cur']=float(m.group(1))
    m=re.search(r'Adjusted net loss per share of \$(\d+\.\d\d)',s,re.I)
    if m: out['eps_cur']=-float(m.group(1))
    else:
        m=re.search(r'Adjusted (?:EPS|loss per share) of \$(\d+\.\d\d)',s,re.I)
        if m: out['eps_cur']=float(m.group(1))
    return out


# ======================= stage 1: assemble events =======================
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")

def qkey(fd):
    """fiscal quarter reported by a filing on date fd (calendar fiscal years for all seven firms)"""
    y, m = int(fd[:4]), int(fd[5:7])
    if m <= 3: return (y - 1, 4)
    if m <= 6: return (y, 1)
    if m <= 9: return (y, 2)
    return (y, 3)

def mid(g): return (g[0] + (g[1] or g[0])) / 2 if g else None

def confirm_eps(r, v):
    h = r.get('head', ''); txt = '%.2f' % abs(v)
    for m in re.finditer(re.escape(txt), h):
        if re.search(r'adjust', h[max(0, m.start() - 170):m.start()], re.I): return True
    return False

def lag_row(L, r, field):
    c = [x for x in L if x['qkey'] == (r['qkey'][0] - 1, r['qkey'][1]) and x['filing_date'] < r['filing_date'] and x.get(field)]
    return c[-1] if c else None

# guidance chains broken on purpose: UNH withdrew its 2025 outlook in May 2025 (no 8-K 2.02 in our list), so the July 2025 "revision" is a re-establishment
GUIDANCE_BREAK = {('UNH', '2025-07-29')}

def load_acceptance(data):
    sub = {}
    for f in glob.glob(data + '/sub/*.json'):
        d = json.load(open(f)); r = d.get('filings', {}).get('recent', d)
        for i, a in enumerate(r['accessionNumber']): sub[a] = r['acceptanceDateTime'][i]
    return sub

def acceptance_et(raw, acc, sub):
    """Eastern acceptance time. The wrapper header (ACCEPTANCE-DATETIME) is Eastern; the submissions JSON is UTC.
    The two agree (UTC = ET + 4 or 5 h) for the 39 filings checked, but for the 19 cover-page-only files the header and the
    JSON differ by 8 to 10 h, so the header is preferred when present and the JSON converted from UTC is the fallback."""
    m = re.search(r'ACCEPTANCE-DATETIME>(\d{14})', raw)
    if m:
        h = m.group(1)
        return datetime.datetime(int(h[:4]), int(h[4:6]), int(h[6:8]), int(h[8:10]), int(h[10:12]), int(h[12:14])), 'header'
    j = sub.get(acc)
    if j:
        t = datetime.datetime.strptime(j[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc).astimezone(ET)
        return t.replace(tzinfo=None), 'json_utc'
    return None, ''

def build_rows(data):
    ev = json.load(open(data + '/earnings8k.json')); sub = load_acceptance(data)
    rows = []
    for t, L in ev.items():
        for fd, acc in L:
            path = f'{data}/rel/{t}_{fd}.htm'
            raw = open(path, errors='ignore').read()
            s = body(prep(path))
            has = bool(re.search(r'per share|earnings|EPS|ratio', s, re.I)) and len(s) > 9000
            r = dict(ticker=t, filing_date=fd, accession=acc, qkey=qkey(fd), has_release=has)
            r['accept_et'], r['accept_src'] = acceptance_et(raw, acc, sub)
            r['timing'], r['timing_src'] = release_timing(r, s if has else '')
            r['headline'], r['flags'] = headline_flags(s) if has else ('', '')
            if has:
                r['mlr_raw'] = mlr(t, s, None); r['head'] = s[:9000]
                r['ci'] = ci_quarter_vals(s) if t == 'CI' else None
                r['eps_raw'] = eps(t, s); r['hum'] = hum_narr(s[:9000]) if t == 'HUM' else None
                c = guid_eps(t, s); r['guid'] = pick_guid(c, t); r['mlr_guid'] = mlr_guid(t, s)
            rows.append(r)
    by = {}
    for r in rows: by.setdefault(r['ticker'], []).append(r)
    for L in by.values(): L.sort(key=lambda r: r['filing_date'])
    for t, L in by.items():
        modal = [x['timing'] for x in L if x['timing_src'] in ('header', 'call_time_in_text')]
        habit = max(set(modal), key=modal.count) if modal else 'pre'
        for r in L:
            if r['timing_src'].startswith('json_utc') and r['accept_et']:
                hm = r['accept_et'].hour * 60 + r['accept_et'].minute
                if 570 <= hm < 960 and r['accept_et'].date().isoformat() == r['filing_date']:
                    r['timing'], r['timing_src'] = habit, 'json_unreliable_midday_used_firm_habit'
    for t, L in by.items():
        for r in L:
            r['mlr'] = None; r['excl'] = ''
            if not r['has_release']: continue
            m = r['mlr_raw']; tab = m.get('tab'); nar = m.get('nar'); c = None
            if tab and nar and abs(tab[0] - nar[0]) <= 0.15 and abs(tab[1] - nar[1]) <= 0.15: c = (tab[0], tab[1], 'table+narrative')
            elif tab and nar: c = (tab[0], tab[1], 'table (narrative differs)')
            elif tab: c = (tab[0], tab[1], 'table')
            elif nar and nar[2] == 'nar': c = (nar[0], nar[1], 'narrative')
            elif nar: c = (nar[0], nar[1], 'narrative_bps')
            if t == 'CI' and c is None:
                d = r.get('ci') or {}; q, y = r['qkey'][1], r['qkey'][0]
                if (q, y) in d and d[(q, y)] > 60:
                    pr = d.get((q, y - 1))
                    c = (d[(q, y)], pr, 'ci_narrative') if pr and pr > 60 else (d[(q, y)], None, 'ci_cur_only')
            if t == 'HUM' and c is None and r['hum'].get('mlr_cur'): c = (r['hum']['mlr_cur'], None, 'hum_narrative_cur')
            r['mlr'] = c
        for r in L:
            if r['mlr']:
                c, p, meth = r['mlr']; lg = lag_row(L, r, 'mlr')
                if p is None and lg: r['mlr'] = (c, lg['mlr'][0], meth + '+prior_from_year_ago_release')
                elif lg and p is not None: r['mlr_lagdiff'] = round(p - lg['mlr'][0], 2)
        for r in L:
            if r['mlr'] and r['mlr'][2] == 'narrative_bps' and abs(r.get('mlr_lagdiff', 0)) > 0.35:
                c = r['mlr']; lg = lag_row(L, r, 'mlr')
                r['mlr'] = (c[0], lg['mlr'][0], 'narrative_cur+prior_from_year_ago_release') if lg else None
        if t == 'CI':
            for r in L:
                if r['filing_date'] <= '2020-02-06':
                    r['mlr'] = None; r['eps_raw'] = None; r['guid'] = None; r['excl'] = 'CI 2019: Express Scripts restructuring, no comparable year-ago base'
        for r in L:
            r['eps'] = None
            if not r['has_release'] or r['excl']: continue
            e = r.get('eps_raw')
            if not e and t == 'HUM' and r['hum'].get('eps_cur') is not None:
                lg = lag_row(L, r, 'eps')
                if lg: e = (r['hum']['eps_cur'], lg['eps'][0], 'hum_narrative')
            if not e: continue
            if confirm_eps(r, e[0]): r['eps'] = (e[0], e[1], 'confirmed')
            else: r['eps_unconf'] = e
        for r in L:
            r['type'] = 'nodoc' if not r['has_release'] else ('full' if (r['eps'] or r['mlr']) else 'no_quarter_results')
            if r['type'] != 'full' and r['has_release']: r['guid'] = None
            r['guid_fy'] = r['qkey'][0] + (1 if r['qkey'][1] == 4 else 0)
            g = r.get('guid') if r['has_release'] else None
            for k in ('eps', 'eps_unconf'):
                if g and r.get(k) and (abs(mid(g) - r[k][0]) < 0.006 or abs(mid(g) - r[k][1]) < 0.006): g = None
            r['guid'] = g; r['gmid'] = mid(g) if g else None
        for r in L:
            r['guid_rev'] = None; r['guid_prev'] = None; r['guid_forms'] = ''
            if r['gmid'] and (t, r['filing_date']) not in GUIDANCE_BREAK:
                prev = [x for x in L if x['filing_date'] < r['filing_date'] and x['gmid'] and x['guid_fy'] == r['guid_fy']]
                if prev and (r['qkey'][0] * 4 + r['qkey'][1]) - (prev[-1]['qkey'][0] * 4 + prev[-1]['qkey'][1]) > 1: prev = []   # a release is missing in between
                if prev:
                    p = prev[-1]; r['guid_prev'] = p['gmid']; r['guid_rev'] = 100 * (r['gmid'] / p['gmid'] - 1)
                    r['guid_forms'] = p['guid'][2] + '->' + r['guid'][2]
    return rows

FLAG_PATTERNS = [('CEO change', r'(?:chief executive officer|CEO)[^.|]{0,90}(?:retire|resign|step(?:s|ped)? down|succe|appoint|new )|(?:retire|resign|step(?:s|ped)? down|succe|appoint)[^.|]{0,90}(?:chief executive officer|CEO)'),
                 ('DOJ/investigation', r'Department of Justice|\bDOJ\b|subpoena|criminal|civil investigative demand|investigation'),
                 ('acquisition/divestiture', r'\bacqui(?:sition|re|red|ring)\b|\bmerger\b|\bdivest\w*|sale of'),
                 ('guidance withdrawn/suspended', r'(?:withdr[ae]w\w*|suspend\w*)[^.|]{0,70}(?:outlook|guidance)|(?:outlook|guidance)[^.|]{0,70}(?:withdr[ae]w\w*|suspend\w*)'),
                 ('cyberattack', r'cyber ?attack'), ('COVID', r'COVID')]

def headline_flags(s):
    m = re.search(r'((?:[A-Z][\w&.\'’-]+ ){1,5}(?:Reports|REPORTS|Delivers|Announces|ANNOUNCES|Provides|Releases|Re-Establishes|Raises|Cuts|Updates|Issues|Posts)[^|•]{8,170})', s[:4500])
    head = re.sub(r'\s+', ' ', m.group(1))[:170] if m else ''
    seg = s[:6000]; fl = [name for name, pat in FLAG_PATTERNS if re.search(pat, seg, re.I)]
    return head, '; '.join(fl)

COLS = ['ticker', 'filing_date', 'accession', 'accept_et', 'accept_src', 'timing', 'timing_src', 'fq_year', 'fq', 'release_text', 'event_type', 'excluded',
        'mlr_cur', 'mlr_prior', 'mlr_method', 'eps_cur', 'eps_prior', 'eps_method', 'guid_fy', 'guid_lo', 'guid_hi', 'guid_form',
        'guid_mid', 'guid_prev_mid', 'guid_rev_pct', 'guid_forms', 'mlr_guided_mid', 'flags', 'headline']

def write_extract(rows, out):
    with open(out, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(COLS)
        for r in sorted(rows, key=lambda r: (r['ticker'], r['filing_date'])):
            m = r['mlr'] or (None, None, ''); e = r['eps'] or (None, None, ''); g = r.get('guid') or (None, None, '')
            w.writerow([r['ticker'], r['filing_date'], r['accession'], r['accept_et'].strftime('%Y-%m-%d %H:%M') if r['accept_et'] else '', r['accept_src'], r['timing'], r['timing_src'],
                        r['qkey'][0], r['qkey'][1], 'yes' if r['has_release'] else 'no (cover page only)', r['type'], r['excl'],
                        m[0], m[1], m[2], e[0], e[1], e[2], r['guid_fy'], g[0], g[1], g[2],
                        None if r['gmid'] is None else round(r['gmid'], 4), r['guid_prev'], None if r['guid_rev'] is None else round(r['guid_rev'], 3), r['guid_forms'],
                        r.get('mlr_guid'), r.get('flags', ''), r.get('headline', '')])


MONTHS = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])}

def call_info(s, fd):
    """first conference-call time in the release text: (minutes after midnight ET, 'same'|'later'|'earlier'|'today') or None"""
    for m in re.finditer(r'(\d{1,2})(?::(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)\s*\(?\s*(?:Eastern|ET\b|EDT|EST|E\.T\.)', s, re.I):
        ctx = s[max(0, m.start() - 260):m.end() + 140]
        if not re.search(r'conference call|teleconference|call (?:for|with) investors|call to', ctx, re.I): continue
        hh, mm, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3).lower()
        if hh < 1 or hh > 12: continue
        mins = (hh % 12) * 60 + mm + (720 if ap.startswith('p') else 0)
        win = s[max(0, m.start() - 160):m.end() + 160]
        d = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s*(20\d\d)', win)
        if re.search(r'\btoday\b', win, re.I): rel = 'today'
        elif d:
            cd = datetime.date(int(d.group(3)), MONTHS[d.group(1).lower()], int(d.group(2)))
            fdd = datetime.date.fromisoformat(fd)
            rel = 'same' if cd == fdd else ('later' if cd > fdd else 'earlier')
        else: rel = 'today'
        return mins, rel
    return None

def release_timing(r, s):
    """'pre' = released before the 9:30 ET open on the filing date; 'post' = at or after the open (day 0 is then the next trading day)"""
    t = r['accept_et']; ci = call_info(s, r['filing_date']) if s else None
    by_hdr = None
    if r['accept_src'] == 'header' and t:
        by_hdr = 'pre' if (t.date().isoformat() == r['filing_date'] and t.hour * 60 + t.minute < 570) else 'post'
        if t.date().isoformat() != r['filing_date'] and t.date().isoformat() < r['filing_date']: by_hdr = 'pre'
    by_call = None
    if ci:
        mins, rel = ci
        if rel in ('today', 'same'): by_call = 'pre' if mins <= 570 else ('post' if mins >= 720 else None)
        elif rel == 'later': by_call = 'post'      # call on a later day: results came out after the close of the filing date
    if by_hdr: return by_hdr, 'header' + ('' if by_call in (None, by_hdr) else ' (call text disagrees)')
    if by_call: return by_call, 'call_time_in_text'
    if t:
        return ('pre' if t.date().isoformat() == r['filing_date'] and t.hour * 60 + t.minute < 570 else 'post'), 'json_utc_converted'
    return 'post', 'default'


# ======================= stage 2: returns, regressions, cynic test =======================
def num(x):
    try:
        v = float(x); return v if v == v else None
    except (TypeError, ValueError):
        return None

def load_prices(data, tickers):
    def one(t):
        d = json.load(open(f'{data}/prices/{t}.json'))['chart']['result'][0]
        ac = d['indicators']['adjclose'][0]['adjclose']
        return {datetime.datetime.fromtimestamp(ts, ET).date().isoformat(): a for ts, a in zip(d['timestamp'], ac) if a}
    mkt = one('XLV'); out = {}
    for t in tickers:
        px = one(t); dates = sorted(set(px) & set(mkt))
        a = np.array([px[x] for x in dates]); b = np.array([mkt[x] for x in dates])
        out[t] = dict(dates=dates, r=a[1:] / a[:-1] - 1, m=b[1:] / b[:-1] - 1, rd=dates[1:])   # return i belongs to date rd[i]
    return out

def ols(y, X, clusters=None, names=None):
    """OLS with intercept already in X. Returns coef, HC1 se, and one se per clustering (CR1)."""
    n, k = X.shape; XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; u = y - X @ b
    out = dict(b=b, n=n, k=k)
    out['r2'] = 1 - (u @ u) / (((y - y.mean()) ** 2).sum()) if n > 1 else float('nan')
    meat = (X * u[:, None]).T @ (X * u[:, None]); out['se_hc1'] = np.sqrt(np.diag(XtXi @ meat @ XtXi) * n / max(n - k, 1))
    for nm, cl in (clusters or {}).items():
        ids = sorted(set(cl)); G = len(ids); M = np.zeros((k, k))
        for g in ids:
            ix = [i for i, c in enumerate(cl) if c == g]; s = X[ix].T @ u[ix]; M += np.outer(s, s)
        c = G / max(G - 1, 1) * (n - 1) / max(n - k, 1)
        out['se_' + nm] = np.sqrt(np.diag(XtXi @ M @ XtXi) * c); out['G_' + nm] = G
    return out

def fit(rows, ycol, xcols, fe=False):
    keep = [r for r in rows if r.get(ycol) is not None and all(r.get(c) is not None for c in xcols)]
    if len(keep) < len(xcols) + 4: return None
    y = np.array([r[ycol] for r in keep]); cols = [np.ones(len(keep))] + [np.array([r[c] for r in keep]) for c in xcols]
    if fe:
        for t in sorted(set(r['ticker'] for r in keep))[1:]: cols.append(np.array([1.0 if r['ticker'] == t else 0.0 for r in keep]))
    X = np.column_stack(cols)
    res = ols(y, X, clusters=dict(firm=[r['ticker'] for r in keep], quarter=[f"{r['fq_year']}Q{r['fq']}" for r in keep]))
    res['names'] = ['const'] + xcols; res['nobs'] = len(keep); res['rows'] = keep
    return res

def tstat(res, i, which='quarter'): return res['b'][i] / res['se_' + which][i]

def fmt_model(label, res, xcols):
    lines = []
    for i, c in enumerate(xcols, start=1):
        lines.append(f"| {label} | {c} | {res['b'][i]:.3f} | {res['se_hc1'][i]:.3f} | {res['se_firm'][i]:.3f} | {res['se_quarter'][i]:.3f} | {res['nobs']} | {res['r2']:.3f} |")
        label = ''
    return lines

def read_extract(path):
    rows = list(csv.DictReader(open(path)))
    for r in rows:
        for k in ('fq_year', 'fq', 'guid_fy'): r[k] = int(r[k])
        for k in ('mlr_cur', 'mlr_prior', 'eps_cur', 'eps_prior', 'guid_lo', 'guid_hi', 'guid_mid', 'guid_prev_mid', 'guid_rev_pct', 'mlr_guided_mid'): r[k] = num(r[k])
    return rows

def analyze(data, extract, out_csv, report):
    rows = read_extract(extract); tickers = sorted(set(r['ticker'] for r in rows))
    P = load_prices(data, tickers); W = []

    def p(*a):
        s = ' '.join(str(x) for x in a); W.append(s); print(s)

    # ---- event day 0, beta, abnormal returns ----
    for r in rows:
        pr = P[r['ticker']]; dts = pr['rd']
        j = 0
        import bisect
        j = bisect.bisect_left(dts, r['filing_date']) if r['timing'] == 'pre' else bisect.bisect_right(dts, r['filing_date'])
        r['d0i'] = j if j < len(dts) else None
        r['mlr_chg'] = r['mlr_cur'] - r['mlr_prior'] if r['mlr_cur'] is not None and r['mlr_prior'] is not None else None
        r['eps_g'] = None
        if r['eps_cur'] is not None and r['eps_prior'] is not None and r['eps_prior'] > 0:
            r['eps_g_raw'] = 100 * (r['eps_cur'] / r['eps_prior'] - 1); r['eps_g'] = max(-100.0, min(100.0, r['eps_g_raw']))
        r['guid_rev'] = r['guid_rev_pct']
        r['ar0'] = r['ar01'] = r['er0'] = r['er01'] = r['beta'] = r['car2_250'] = r['day0'] = None
        if r['d0i'] is None: continue
        i0 = r['d0i']; r['day0'] = dts[i0]
        cutoff = (datetime.date.fromisoformat(dts[i0]) - datetime.timedelta(days=30)).isoformat()
        e = bisect.bisect_right(dts, cutoff) - 1
        if e - 249 < 0: continue
        ri = pr['r'][e - 249:e + 1]; rm = pr['m'][e - 249:e + 1]
        b = float(np.cov(ri, rm, ddof=1)[0, 1] / np.var(rm, ddof=1)); r['beta'] = b
        ar = pr['r'] - b * pr['m']; ex = pr['r'] - pr['m']
        r['ar0'] = 100 * ar[i0]; r['er0'] = 100 * ex[i0]
        if i0 + 1 < len(ar): r['ar01'] = 100 * ar[i0:i0 + 2].sum(); r['er01'] = 100 * ex[i0:i0 + 2].sum()
        if i0 + 250 < len(ar): r['car2_250'] = 100 * ar[i0 + 2:i0 + 251].sum()
    ev = [r for r in rows if r['ar0'] is not None]
    # ---- timing sanity ----
    p('## Counts')
    p(f"events listed: {len(rows)}; with a computed abnormal return: {len(ev)}; release text available: {sum(r['release_text']=='yes' for r in rows)}")
    full = [r for r in ev if r['event_type'] == 'full']
    p(f"events with quarterly results parsed (event_type=full): {sum(r['event_type']=='full' for r in rows)}; clean MLR yoy: {sum(r['mlr_chg'] is not None for r in rows)}; clean adjusted EPS yoy (prior > 0): {sum(r['eps_g'] is not None for r in rows)}; clean guidance revision: {sum(r['guid_rev'] is not None for r in rows)}")
    for t in tickers:
        L = [r for r in rows if r['ticker'] == t]
        p(f"  {t}: events {len(L)}, release text {sum(r['release_text']=='yes' for r in L)}, MLR {sum(r['mlr_chg'] is not None for r in L)}, EPS {sum(r['eps_g'] is not None for r in L)}, guidance revision {sum(r['guid_rev'] is not None for r in L)}")
    p(f"timing source: " + ', '.join(f"{k}={sum(1 for r in rows if r['timing_src']==k)}" for k in sorted(set(r['timing_src'] for r in rows))))
    p(f"day 0 rule: pre-open -> filing day, else next trading day; pre={sum(r['timing']=='pre' for r in rows)}, post={sum(r['timing']=='post' for r in rows)}")
    p(f"mean beta {np.mean([r['beta'] for r in ev]):.2f}; by firm: " + ', '.join(f"{t}={np.mean([r['beta'] for r in ev if r['ticker']==t]):.2f}" for t in tickers))
    # ---- timing check: does the day chosen from the release text carry the bigger move than the day the acceptance time alone would pick? ----
    def ar_at(r, i0):
        pr = P[r['ticker']]; dts = pr['rd']
        cutoff = (datetime.date.fromisoformat(dts[i0]) - datetime.timedelta(days=30)).isoformat(); e = bisect.bisect_right(dts, cutoff) - 1
        ri = pr['r'][e - 249:e + 1]; rm = pr['m'][e - 249:e + 1]; b = float(np.cov(ri, rm, ddof=1)[0, 1] / np.var(rm, ddof=1))
        return 100 * (pr['r'][i0] - b * pr['m'][i0])
    gA, gB = [], []
    for r in rows:
        dts = P[r['ticker']]['rd']; pre_i = bisect.bisect_left(dts, r['filing_date']); post_i = bisect.bisect_right(dts, r['filing_date'])
        if not r['accept_et'] or post_i >= len(dts) or pre_i < 260: continue
        hm = int(r['accept_et'][11:13]) * 60 + int(r['accept_et'][14:16])
        if r['timing'] == 'pre' and r['timing_src'] in ('call_time_in_text', 'json_unreliable_midday_used_firm_habit') and (hm >= 570 or r['accept_et'][:10] != r['filing_date']):
            gA.append((ar_at(r, pre_i), ar_at(r, post_i)))
        if r['timing'] == 'post' and r['timing_src'] == 'header':
            gB.append((ar_at(r, post_i), ar_at(r, pre_i)))
    p('\n## Timing check (mean absolute day-0 abnormal return, percent)')
    for nm, g in (('release text says before the open but the 8-K was accepted after it: assigned = filing day, alternative = next day', gA), ('header says after the close: assigned = next day, alternative = filing day', gB)):
        if g:
            a = np.abs(np.array(g)); p(f"  {nm}: n={len(g)}; assigned {a[:,0].mean():.2f}, alternative {a[:,1].mean():.2f}; assigned day larger in {np.mean(a[:,0] > a[:,1]):.0%}")
    # ---- descriptive: all events ----
    p('\n## Abnormal returns, all events with prices (percent)')
    p(f"day 0: mean AR {np.mean([r['ar0'] for r in ev]):.2f}, mean |AR| {np.mean([abs(r['ar0']) for r in ev]):.2f}, sd {np.std([r['ar0'] for r in ev], ddof=1):.2f}; simple excess mean {np.mean([r['er0'] for r in ev]):.2f}")
    e1 = [r for r in ev if r['ar01'] is not None]
    p(f"days 0-1: mean AR {np.mean([r['ar01'] for r in e1]):.2f}, sd {np.std([r['ar01'] for r in e1], ddof=1):.2f}")
    # ---- regressions ----
    models = [('M1 MLR only', ['mlr_chg']), ('M2 guidance only', ['guid_rev']), ('M3 EPS only', ['eps_g']), ('M4 MLR + EPS', ['mlr_chg', 'eps_g']), ('M5 all three', ['mlr_chg', 'guid_rev', 'eps_g'])]
    def table(title, sample, ycol, fe=False):
        p(f"\n### {title}"); p('| model | variable | coef | se (HC1) | se (firm cluster) | se (quarter cluster) | n | R2 |'); p('|---|---|---|---|---|---|---|---|')
        for label, xc in models:
            res = fit(sample, ycol, xc, fe=fe)
            if res: [p(l) for l in fmt_model(label, res, xc)]
    sets = {'all events': full}
    p('\n## Regressions: abnormal return (percent) on MLR change (percentage points), guidance revision (percent of midpoint), adjusted EPS growth (percent, winsorized at +-100)')
    table('Day 0, beta-adjusted, pooled', full, 'ar0'); table('Days 0 to +1, beta-adjusted, pooled', full, 'ar01')
    table('Day 0, beta-adjusted, firm fixed effects', full, 'ar0', fe=True); table('Day 0, simple excess return over XLV, pooled', full, 'er0')
    # common sample
    comm = [r for r in full if r['mlr_chg'] is not None and r['guid_rev'] is not None and r['eps_g'] is not None]
    p(f"\ncommon sample with all three regressors: n={len(comm)}"); table('Day 0, common sample', comm, 'ar0')
    # sensitivity
    ex_unh25 = [r for r in full if not (r['ticker'] == 'UNH' and r['filing_date'].startswith('2025'))]
    ex_2020 = [r for r in full if not r['filing_date'].startswith('2020')]
    ex_both = [r for r in ex_unh25 if not r['filing_date'].startswith('2020')]
    ex_base = [r for r in full if r['fq_year'] not in (2020, 2021)]
    table('Day 0, excluding UNH 2025 events', ex_unh25, 'ar0'); table('Day 0, excluding all 2020 events', ex_2020, 'ar0'); table('Day 0, excluding both', ex_both, 'ar0')
    table('Day 0, excluding results for fiscal 2020 and 2021 (pandemic and base-year effects)', ex_base, 'ar0')
    # same-form guidance only
    sf = [dict(r, guid_rev=(r['guid_rev'] if (r['guid_forms'].split('->')[0] == r['guid_forms'].split('->')[-1] or (set(r['guid_forms'].split('->')) <= {'range', 'point'})) else None)) for r in full]
    table('Day 0, guidance revisions only where both releases use the same form (range/point together, or floor to floor)', sf, 'ar0')
    # simple correlation checks
    p('\n### Correlations among regressors (common sample)')
    if len(comm) > 5:
        A = np.array([[r['mlr_chg'], r['guid_rev'], r['eps_g'], r['ar0']] for r in comm]); C = np.corrcoef(A.T)
        p('order: MLR change, guidance revision, EPS growth, AR0'); [p('  ' + ' '.join(f'{v:6.2f}' for v in row)) for row in C]
    # robust: rank-based (Spearman) for MLR
    def spearman(a, b):
        ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b)); return float(np.corrcoef(ra, rb)[0, 1])
    m1 = [r for r in full if r['mlr_chg'] is not None]
    p(f"Spearman(MLR change, AR0) = {spearman([r['mlr_chg'] for r in m1],[r['ar0'] for r in m1]):.2f} (n={len(m1)}); Spearman(guidance revision, AR0) = {spearman([r['guid_rev'] for r in full if r['guid_rev'] is not None],[r['ar0'] for r in full if r['guid_rev'] is not None]):.2f} (n={sum(r['guid_rev'] is not None for r in full)})")
    # nonzero guidance revisions only
    nz = [r for r in full if r['guid_rev'] is not None and abs(r['guid_rev']) > 0.05]
    p(f"revisions that are not zero: n={len(nz)}; of all {sum(r['guid_rev'] is not None for r in full)}; mean AR0 when guidance raised (>0.05%): {np.mean([r['ar0'] for r in nz if r['guid_rev']>0]):.2f} (n={sum(r['guid_rev']>0 for r in nz)}), when cut: {np.mean([r['ar0'] for r in nz if r['guid_rev']<0]):.2f} (n={sum(r['guid_rev']<0 for r in nz)}); unchanged: {np.mean([r['ar0'] for r in full if r['guid_rev'] is not None and abs(r['guid_rev'])<=0.05]):.2f} (n={sum(r['guid_rev'] is not None and abs(r['guid_rev'])<=0.05 for r in full)})")
    # MLR buckets
    p('\n### Day-0 abnormal return by MLR change bucket (percentage points)')
    p('| bucket | n | mean AR0 | median AR0 |'); p('|---|---|---|---|')
    for lab, lo, hi in [('fell by 1 or more', -99, -1), ('between -1 and +1', -1, 1), ('rose 1 to 3', 1, 3), ('rose 3 or more', 3, 99)]:
        g = [r['ar0'] for r in m1 if lo <= r['mlr_chg'] < hi]
        if g: p(f"| {lab} | {len(g)} | {np.mean(g):.2f} | {np.median(g):.2f} |")
    # ---- top lists ----
    def row_desc(r):
        return (f"| {r['ticker']} | {r['filing_date']} | {r['ar0']:.1f} | {'' if r['ar01'] is None else format(r['ar01'],'.1f')} | "
                f"{'' if r['mlr_chg'] is None else format(r['mlr_chg'],'+.1f')} | {'' if r['guid_rev'] is None else format(r['guid_rev'],'+.1f')} | "
                f"{'' if r['eps_g'] is None else format(r['eps_g'],'+.0f')} | {r['flags'] or ''} | {(r['headline'] or '')[:90]} |")
    srt = sorted(ev, key=lambda r: r['ar0'])
    p('\n## Ten largest negative and positive day-0 abnormal returns (all events with prices)')
    for lab, grp in (('negative', srt[:10]), ('positive', srt[::-1][:10])):
        p(f"\n{lab}"); p('| firm | filing date | AR day 0 (%) | AR days 0-1 (%) | MLR chg (pp) | guidance rev (%) | EPS growth (%) | release-text flags | headline |'); p('|---|---|---|---|---|---|---|---|---|')
        for r in grp: p(row_desc(r))
    top20 = sorted(ev, key=lambda r: -abs(r['ar0']))[:20]
    p(f"\nof the 20 largest absolute day-0 moves, {sum(r['mlr_chg'] is not None for r in top20)} have a parsed MLR change, {sum(r['guid_rev'] is not None for r in top20)} a guidance revision; {sum(r['release_text']!='yes' for r in top20)} have no release text (cover page only): " + ', '.join(f"{r['ticker']} {r['filing_date']}" for r in top20 if r['release_text']!='yes'))
    p(f"share of all absolute day-0 movement (sum of |AR0|) in events without a parsed MLR: {sum(abs(r['ar0']) for r in ev if r['mlr_chg'] is None)/sum(abs(r['ar0']) for r in ev):.0%}")
    # ---- cynic test ----
    p('\n## Cynic test (exploratory)')
    idx = {(r['ticker'], r['fq_year'], r['fq']): r for r in rows if r['event_type'] == 'full' and r['mlr_cur'] is not None}
    spikes = [r for r in rows if r['mlr_chg'] is not None and r['mlr_chg'] >= 1.0 and r['ar0'] is not None]
    others = [r for r in rows if r['mlr_chg'] is not None and r['mlr_chg'] < 1.0 and r['ar0'] is not None]
    p(f"events with MLR up 1 pp or more year on year: {len(spikes)}; other events with an MLR: {len(others)}")
    def back(r):
        n4 = idx.get((r['ticker'], r['fq_year'] + 1, r['fq']))
        return (n4['mlr_cur'] - r['mlr_cur']) if n4 else None
    for r in rows: r['mlr_t4'] = back(r) if r['mlr_chg'] is not None else None
    def back_same(r):
        n4 = idx.get((r['ticker'], r['fq_year'] + 1, r['fq']))
        return n4['mlr_chg'] if n4 and n4['mlr_chg'] is not None else None
    for r in rows: r['mlr_t4_same'] = back_same(r) if r['mlr_chg'] is not None else None
    def summ(g, key):
        v = [r[key] for r in g if r[key] is not None]
        return v
    for lab, g in (('spikes (>= +1 pp)', spikes), ('other events', others), ('spikes excluding 2021 events (year-ago base was 2020)', [r for r in spikes if r['fq_year'] != 2021]), ('spikes excluding 2020 and 2021 base years', [r for r in spikes if r['fq_year'] not in (2020, 2021)]), ('other events excluding 2020 and 2021 base years', [r for r in others if r['fq_year'] not in (2020, 2021)])):
        v = summ(g, 'mlr_t4')
        if v: p(f"(a) {lab}: n with a t+4 quarters ratio = {len(v)} of {len(g)}; mean change in the ratio from t to t+4 = {np.mean(v):+.2f} pp; share that fell = {np.mean([x<0 for x in v]):.0%}; share that fell by at least 1 pp = {np.mean([x<=-1 for x in v]):.0%}")
    p('    same-definition version (the release at t+4 reports the restated quarter-t ratio as its year-ago value, so its own year-on-year change is the change from t to t+4):')
    for lab, g in (('spikes', spikes), ('spikes excluding 2020 and 2021 base years', [r for r in spikes if r['fq_year'] not in (2020, 2021)]), ('other events excluding 2020 and 2021 base years', [r for r in others if r['fq_year'] not in (2020, 2021)])):
        v = summ(g, 'mlr_t4_same')
        if v: p(f"      {lab}: n={len(v)}; mean change {np.mean(v):+.2f} pp; share that fell {np.mean([x<0 for x in v]):.0%}; share that fell by at least 1 pp {np.mean([x<=-1 for x in v]):.0%}")
    sp4 = [r for r in spikes if r['mlr_t4'] is not None]
    # back to the year-ago level?
    ret = []
    for r in sp4:
        n4 = idx[(r['ticker'], r['fq_year'] + 1, r['fq'])]; ret.append(n4['mlr_cur'] - r['mlr_prior'])
    if ret: p(f"    t+4 ratio minus the year-ago (pre-spike) ratio, spikes with t+4: mean {np.mean(ret):+.2f} pp; back within 0.5 pp of the pre-spike level or lower in {np.mean([x<=0.5 for x in ret]):.0%} of {len(ret)}")
    p('    spike list (firm, date, MLR change, ratio at t+4 minus ratio at t):'); [p(f"      {r['ticker']} {r['filing_date']} chg {r['mlr_chg']:+.1f}  t+4 {'' if r['mlr_t4'] is None else format(r['mlr_t4'],'+.1f')}") for r in spikes]
    # (b) CAR 2..250
    sp_c = [r['car2_250'] for r in spikes if r['car2_250'] is not None]; ot_c = [r['car2_250'] for r in others if r['car2_250'] is not None]
    all_c = [r['car2_250'] for r in ev if r['car2_250'] is not None]
    def welch(a, b):
        if len(a) < 2 or len(b) < 2: return float('nan')
        return (np.mean(a) - np.mean(b)) / math.sqrt(np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b))
    p(f"(b) CAR day +2 to +250 (beta-adjusted, percent): spikes n={len(sp_c)} mean {np.mean(sp_c):+.1f} median {np.median(sp_c):+.1f}; other events with an MLR n={len(ot_c)} mean {np.mean(ot_c):+.1f} median {np.median(ot_c):+.1f}; all events n={len(all_c)} mean {np.mean(all_c):+.1f}; naive Welch t (spikes minus others) = {welch(sp_c, ot_c):.2f}")
    # regression of CAR on spike dummy with firm and quarter clusters
    for r in rows: r['spike'] = (1.0 if r['mlr_chg'] >= 1.0 else 0.0) if r['mlr_chg'] is not None else None
    rr = fit([r for r in rows if r['car2_250'] is not None], 'car2_250', ['spike'])
    if rr: p(f"    regression CAR[2,250] on spike dummy: coef {rr['b'][1]:+.1f}, se firm {rr['se_firm'][1]:.1f}, se quarter {rr['se_quarter'][1]:.1f}, n={rr['nobs']} (windows overlap heavily within firm: the effective sample is much smaller)")
    rr2 = fit([r for r in rows if r['car2_250'] is not None], 'car2_250', ['mlr_chg'])
    if rr2: p(f"    regression CAR[2,250] on MLR change: coef {rr2['b'][1]:+.2f} per pp, se firm {rr2['se_firm'][1]:.2f}, se quarter {rr2['se_quarter'][1]:.2f}, n={rr2['nobs']}")
    rr3 = fit([r for r in rows if r['car2_250'] is not None and r['fq_year'] not in (2020, 2021)], 'car2_250', ['spike'])
    if rr3: p(f"    same regression excluding 2020 and 2021 events (COVID base years): coef {rr3['b'][1]:+.1f}, se firm {rr3['se_firm'][1]:.1f}, se quarter {rr3['se_quarter'][1]:.1f}, n={rr3['nobs']}")
    rr4 = fit([r for r in rows if r['car2_250'] is not None and r['fq_year'] not in (2020, 2021)], 'car2_250', ['mlr_chg'])
    if rr4: p(f"    CAR[2,250] on MLR change excluding 2020 and 2021 events: coef {rr4['b'][1]:+.2f} per pp, se firm {rr4['se_firm'][1]:.2f}, se quarter {rr4['se_quarter'][1]:.2f}, n={rr4['nobs']}")
    sp_nobase = [r['car2_250'] for r in spikes if r['car2_250'] is not None and r['fq_year'] not in (2020, 2021)]
    p(f"    spikes excluding 2020 and 2021 base years: n={len(sp_nobase)} mean {np.mean(sp_nobase) if sp_nobase else float('nan'):+.1f}")
    p('    spike list (firm, date, CAR 2..250):'); [p(f"      {r['ticker']} {r['filing_date']} {'' if r['car2_250'] is None else format(r['car2_250'],'+.1f')}") for r in spikes]
    # (c) next full-year guidance
    gi = {}
    for r in rows:
        if r['guid_mid'] is not None: gi.setdefault((r['ticker'], r['guid_fy']), []).append(r)
    def next_growth(r):
        if r['guid_mid'] is None: return None
        cur = sorted(gi.get((r['ticker'], r['guid_fy']), []), key=lambda x: x['filing_date'])
        nxt = sorted(gi.get((r['ticker'], r['guid_fy'] + 1), []), key=lambda x: x['filing_date'])
        if not nxt: return None
        last = [x for x in cur][-1]
        return 100 * (nxt[0]['guid_mid'] / last['guid_mid'] - 1), last['guid_form'] + '->' + nxt[0]['guid_form']
    for r in rows:
        r['next_guid_growth'] = None
        if r['mlr_chg'] is not None:
            g = next_growth(r)
            if g: r['next_guid_growth'] = g[0]
    sg = [r for r in spikes if r['next_guid_growth'] is not None]; og = [r for r in others if r['next_guid_growth'] is not None]
    p(f"(c) initial guidance midpoint for the next fiscal year vs the last guidance midpoint of the spike's fiscal year (percent): spikes n={len(sg)} mean {np.mean([r['next_guid_growth'] for r in sg]) if sg else float('nan'):+.1f}, share above zero {np.mean([r['next_guid_growth']>0 for r in sg]) if sg else float('nan'):.0%}; other events n={len(og)} mean {np.mean([r['next_guid_growth'] for r in og]):+.1f}, share above zero {np.mean([r['next_guid_growth']>0 for r in og]):.0%}")
    sg2 = [r for r in sg if r['fq_year'] not in (2020, 2021)]; og2 = [r for r in og if r['fq_year'] not in (2020, 2021)]
    p(f"    excluding 2020 and 2021 events: spikes n={len(sg2)} mean {np.mean([r['next_guid_growth'] for r in sg2]):+.1f}, share above zero {np.mean([r['next_guid_growth']>0 for r in sg2]):.0%}; others n={len(og2)} mean {np.mean([r['next_guid_growth'] for r in og2]):+.1f}, share above zero {np.mean([r['next_guid_growth']>0 for r in og2]):.0%}")
    p(f"    unique firm-fiscal-years: spikes {len(set((r['ticker'], r['guid_fy']) for r in sg))} (of n={len(sg)}), others {len(set((r['ticker'], r['guid_fy']) for r in og))} (of n={len(og)}); excluding 2020 and 2021: spikes {len(set((r['ticker'], r['guid_fy']) for r in sg2))}, others {len(set((r['ticker'], r['guid_fy']) for r in og2))}")
    p('    spike list (firm, date, next-year guidance vs this-year last guidance %):'); [p(f"      {r['ticker']} {r['filing_date']} {r['next_guid_growth']:+.1f}") for r in sg]
    # ---- write per-event CSV ----
    keys = ['ticker', 'filing_date', 'fq_year', 'fq', 'event_type', 'release_text', 'timing', 'timing_src', 'accept_et', 'day0', 'beta', 'ar0', 'ar01', 'er0', 'er01', 'car2_250',
            'mlr_cur', 'mlr_prior', 'mlr_chg', 'mlr_method', 'eps_cur', 'eps_prior', 'eps_g_raw', 'eps_g', 'guid_fy', 'guid_form', 'guid_mid', 'guid_prev_mid', 'guid_rev', 'guid_forms',
            'mlr_guided_mid', 'mlr_t4', 'mlr_t4_same', 'next_guid_growth', 'excluded', 'flags', 'headline', 'accession']
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(keys)
        for r in sorted(rows, key=lambda r: (r['filing_date'], r['ticker'])):
            w.writerow([('' if r.get(k) is None else (round(r[k], 4) if isinstance(r.get(k), float) else r.get(k))) for k in keys])
    if report: open(report, 'w').write('\n'.join(W) + '\n')

def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('stage', choices=['extract', 'analyze'])
    ap.add_argument('--data', required=True, help='folder with earnings8k.json, rel/, sub/, prices/')
    ap.add_argument('--out', required=True); ap.add_argument('--extract'); ap.add_argument('--report')
    a = ap.parse_args()
    if a.stage == 'extract':
        rows = build_rows(a.data); write_extract(rows, a.out); print(f'{len(rows)} events written to {a.out}')
    else:
        global np
        import numpy as np
        analyze(a.data, a.extract, a.out, a.report)

if __name__ == '__main__':
    main()
