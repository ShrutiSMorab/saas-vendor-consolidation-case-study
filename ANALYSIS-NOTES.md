# Analysis notes

The reasoning behind the model, including the parts that did not make the deck and the numbers I am least sure of.

## What I fixed in the brief before I trusted it

The original brief adds three savings buckets to reach its total: remove unused licences, consolidate duplicates, and negotiate enterprise pricing. Those buckets overlap. If the strategy retires Monday.com and Trello outright, then the unused licences on those tools and the duplicate seats on them are already inside the retirement number. Counting them again as separate line items inflates the total.

So I did not add buckets. I modelled one end state, priced it, and took the difference from current spend. That is the only way to get a savings figure that does not double count, and it is the version that survives Finance asking how you got it.

The brief's narrative also says $3.2M in one place and the table totals $2.37M. I scoped the case to the four addressable PM tools at $2.37M and left the wider collaboration footprint out. If the real number is $3.2M there is more to go at, but I would rather under-claim on a number I can stand behind.

## The end-state build

Standardise on Asana, retire Monday.com and Trello, keep Jira ring-fenced for Engineering.

Asana end-state seats: I take the 510 current Asana active users and add the users migrating off Monday.com (230 active) and Trello (120 active), which is 350 people to rehome. Not all of them need a new seat, because some already hold Asana as part of the duplicate-licence problem. I estimate 150 of the 350 already have Asana, so net-new seats added is 200, and the end-state Asana count is 710.

End-state cost: 710 seats at a negotiated $1,000 is $710,000 for Asana, plus Jira held flat at $1,050,000, for $1,760,000 total. Current spend is $2,370,000. Base-case saving is $610,000, or 25.7%.

## The savings bridge, lever by lever

The bridge in the workbook and on the deck reconciles current spend to end state through five moves, each isolated so none is counted twice:

1. Remove 140 unused Asana licences (650 purchased, 510 active) at list rate: minus $168,000.
2. Retire Trello: minus $120,000.
3. Retire Monday.com: minus $420,000.
4. Migrate 200 net-new users onto Asana at the negotiated $1,000 rate: plus $200,000.
5. Renegotiate the rate on the 510 retained Asana seats from $1,200 to $1,000: minus $102,000.

The migrated seats in step 4 are already priced at the negotiated rate, so the rate cut in step 5 applies only to the retained seats. That is the discipline that stops the double count.

## The range

I do not report a single number, because a single number on a modelled negotiation is a false precision. The range moves with two levers, the Asana rate and whether Jira gets right-sized at its renewal:

- Conservative, $540K. Asana at $1,100 (a weak 8% off list) and Jira untouched. This happens to match the brief's own figure, and it is the number I would quote cold in an interview because it needs the least defending.
- Base, $610K. Asana at $1,000 on a three-year deal and Jira untouched.
- Optimistic, $750K. Asana at $950 and Jira right-sized 10% at its renewal.

## The numbers I am least sure of, in order

1. **The 150-person overlap.** This is the softest input in the whole model. I estimated how many of the Monday.com and Trello users already hold Asana, and the real figure needs a licence-to-headcount join that the brief does not provide. If the overlap is smaller, I add more Asana seats and save less. If it is larger, I save more. It moves the answer, so it is flagged here rather than buried.

2. **Jira.** The brief gives no active-user count for Jira, which is 44% of total spend. That is the single biggest blind spot in the case. Engineering will not move off it and I am not proposing they do, but I cannot rule out that Jira carries idle seats of its own. The base case assumes zero Jira savings precisely because I have no data to claim any. The first thing I would do in the real role is audit it.

3. **The negotiated Asana rate.** Modelled from list price and deal shape, not quoted. Covered in the negotiation file.

## What I would add if this were real

- A supplier risk view. Standardising four tools down to two concentrates risk onto Asana and Jira. That is a fair trade for the saving and the simplicity, but it should be a conscious decision with a documented exit path, not a side effect.
- The change-management cost. Migrating Monday.com and Trello users onto Asana is not free. There is admin time, training and a productivity dip during the switch. I pushed to have Asana fund the training as part of the deal, which offsets it, but a real business case would carry a one-off migration cost line against the recurring saving.
- A usage-based true-up. The flex-down clause I want in the Asana contract only works if someone watches utilisation each quarter. The governance is as important as the negotiation.

## Reproduce it

```
pip install matplotlib pandas openpyxl
python analysis.py        # regenerates the six charts
python build_xlsx.py      # rebuilds the model
```

The workbook's blue cells are the levers. Change the Asana rate or the overlap estimate and every sheet, including the savings bridge and the scenario range, recalculates.
