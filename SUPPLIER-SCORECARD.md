# Supplier scorecard

Four vendors, scored 1 to 5 against weighted criteria drawn from what Meridian actually needs from a PM platform. The weights are mine. I set them before scoring so the ranking could not be reverse-engineered to a conclusion I already wanted.

## Weights and scores

| Criterion | Weight | Asana | Jira | Monday.com | Trello |
| --- | --- | --- | --- | --- | --- |
| User adoption / breadth of fit | 20% | 4 | 3 | 3 | 2 |
| Commercial flexibility | 15% | 4 | 3 | 3 | 2 |
| Integrations | 15% | 4 | 5 | 3 | 2 |
| Security | 15% | 4 | 5 | 3 | 3 |
| GDPR compliance | 10% | 4 | 4 | 4 | 3 |
| Support | 10% | 4 | 4 | 3 | 2 |
| Product roadmap | 10% | 4 | 4 | 4 | 2 |
| Scalability | 5% | 4 | 5 | 3 | 2 |
| **Weighted total (of 5)** | | **4.00** | **4.00** | **3.20** | **2.25** |

## The number that matters is not the top number

Asana and Jira tie at 4.00, and that tie is the whole point of the scorecard.

Read Jira's column. Its 4.00 is carried by integrations, security and scalability, all scored 5. Those are the things that matter to a software engineering org with a toolchain wired into its issue tracker. They do very little for a marketer or an HR coordinator who needs a shared board and a task list. Jira scores 3 on breadth of fit for exactly that reason. It is an excellent tool for the people who need it and an awkward one for everyone else.

Asana gets to the same 4.00 by scoring evenly. Nothing world-beating, nothing weak, and a 4 on the criterion that carries the most weight, breadth of fit. That is the profile you want for a single standard tool that has to serve Product, Marketing, HR and Operations at once.

So the scorecard does not say "pick the highest score and standardise on it." It says Jira wins for Engineering on the criteria Engineering cares about, and Asana wins as the general standard for everyone else. That is the recommendation. A scorecard read naively would have merged them into one tool and broken one side or the other.

Monday.com at 3.20 is a competent middle. It does nothing badly, but it does not beat Asana on any weighted criterion, so on a consolidation play it loses to the tool that already has the largest active base.

Trello at 2.25 is the clear retire. It is lightweight by design, which is fine as a free tier and hard to justify at $120,000 of Enterprise licensing when its 120 active users can be rehomed onto the standard tool.

## What I would add before signing anything

The scores are my judgement from the vendors' public posture and general market reputation, not from a live RFP with security questionnaires returned and reference calls made. Before a real award I would want SOC 2 and ISO 27001 evidence in hand, data-residency confirmation for the EU, and the integration list checked against our actual stack rather than assumed. The ranking would probably hold. The point is that it should be earned against returned evidence, not asserted from a table.
