import re

NOINDEX = '<meta name="robots" content="noindex,nofollow">\n'

CUST_SEC = '''<!-- 6 -->
<section id="customers"><div class="wrap">
  <h2><span class="num">6</span>The Customers</h2>
  <div class="lead">Family-owned banana ripeners and importers across the Northeast — a small, named universe (not a numbers game).</div>
  <p>Our customers buy full truckloads of Dole/Chiquita bananas out of the Port of Wilmington and ripen them in-house. They're multi-generational, relationship-driven, often voice-first and old-school. There are only a few dozen realistic targets — so the sales game is <b>depth, not volume.</b></p>
  <div class="callout gold"><b>TAM (Total Addressable Market):</b> the whole pie of customers we could ever serve. Ours is tiny and we know every name. <b>The specific customer list (names, locations, contacts) is confidential — it's in the internal playbook. Ask Amedeo on day one.</b></div>
</div></section>

'''

TARGETS_SEC = '''<!-- 9 -->
<section id="targets"><div class="wrap">
  <h2><span class="num">9</span>Your Target List</h2>
  <div class="lead">The banana-customer universe is a small, named set of family companies — that's your hit list.</div>
  <div class="callout gold"><b>The live target list — existing customers, hot prospects, contacts, and tiers — is confidential and lives in the internal playbook.</b> Ask Amedeo for it on day one. Your job: work those named relationships with depth, leveraging warm intros and the produce-community network (PDA, the wholesale markets).</div>
</div></section>

'''

# customer/prospect name -> generic
NAMES = {
 "Yell-O-Glow":"a Boston-area customer","Cedro Bananas":"a customer","Cedro":"a customer",
 "Newburgh Banana":"a customer","Top Banana":"a customer","Top Distributing":"a customer",
 "Northeast Banana":"a customer","Kapi Kapi Growers":"a customer","Kapi Kapi":"a customer","Kapi":"a customer","Ayco Farms":"a customer","Ayco":"a customer",
 "M. Levin & Co":"a top prospect","M. Levin":"a top prospect","New England Banana":"a prospect",
 "EXP Group":"a prospect","John Vena":"a prospect","Class Produce":"a prospect","Westwood Banana":"a prospect","Westwood":"a prospect",
 "E. Armata":"a prospect","D'Arrigo":"a prospect","Wegmans":"a national retailer","Procacci":"a prospect",
 "David Levin":"the decision-maker","Mark Levin":"the owner","Anthony Serafino":"the president",
}
# sensitive customer-rate / margin figures -> placeholder
NUMS = {"$1,900.00":"$X,XXX","$1,900":"$X,XXX","$1,740":"$X,XXX","~$300–$500":"~$XXX","$300–$500":"$XXX",
        "$284":"$XXX","$167":"$XXX","$117":"$XXX"}

def scrub(path, is_part1=False, is_part2=False, is_test=False):
    s = open(path,encoding="utf-8").read()
    # noindex
    s = s.replace("</title>","</title>\n"+NOINDEX,1)
    if is_part1:
        s = re.sub(r'<!-- 6 -->.*?(?=<!-- 7 -->)', CUST_SEC, s, flags=re.S)
    if is_part2:
        s = re.sub(r'<!-- 9 -->.*?(?=<!-- 10 -->)', TARGETS_SEC, s, flags=re.S)
    if is_test:
        # replace the M. Levin question object
        s = re.sub(r'\{s:"Selling", q:"Your hottest cold banana lead.*?\}\n\];',
            '''{s:"Selling", q:"On a banana-customer cold call, the right first move is to:",
  o:["Open with your lowest rate","Lead with local/relationship proof, then ask who handles their drayage","Email a long company brochure","Pitch a 12-month contract immediately"], a:1,
  e:"Family banana houses are relationship-first — lead with proof you already serve their world, then ask who handles their port drayage."}
];''', s, flags=re.S)
    for k,v in NAMES.items(): s = s.replace(k,v)
    for k,v in NUMS.items(): s = s.replace(k,v)
    open(path,"w",encoding="utf-8").write(s)
    print(f"scrubbed {path} ({len(s)} bytes)")

scrub("operations.html", is_part1=True)
scrub("playbook.html", is_part2=True)
scrub("test.html", is_test=True)
