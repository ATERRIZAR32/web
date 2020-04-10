from django.utils import timezone

from grants.models import *
from grants.models import Contribution, PhantomFunding
from grants.views import next_round_start, round_end

# total stats

start = next_round_start
end = round_end

contributions = Contribution.objects.filter(created_on__gt=start, created_on__lt=end, success=True)
contributions = contributions.filter(subscription__grant__grant_type='health')

stats = {}

for contrib in contributions:
    key = contrib.subscription.grant.title
    if key not in stats.keys():
        match_amount = 0
        try:
            match_amount = contrib.subscription.grant.clr_prediction_curve[0][1]
        except:
            pass
        stats[key] = {
            'url': "https://gitcoin.co" + contrib.subscription.grant.url,
            'match_amount': match_amount,
            'contributions': [],
            'contributions_per_profile': [],
            'contributions_per_originated_address': [],
            'contributions_without_originated_address': [],
        }
    stats[key]['contributions'].append(contrib.pk)
    stats[key]['contributions_per_profile'].append(contrib.subscription.contributor_profile.pk)
    stats[key]['contributions_per_originated_address'].append(contrib.originated_address)
    if contrib.originated_address == '0x0':
        stats[key]['contributions_without_originated_address'].append(contrib.pk)


print("url, title, match amount, contributions, contributors by profile, contributors by originated_address, contributions without originated address")
for key, pkg in stats.items():
    print(
        pkg['url'], ",",
        key, ",",
        ((pkg['match_amount'])), ",",
        len(set(pkg['contributions'])), ",",
        len(set(pkg['contributions_per_profile'])), ",",
        len(set(pkg['contributions_per_originated_address'])), ",",
        len(set(pkg['contributions_without_originated_address'])), ",",
        )
 