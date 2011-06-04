from canopy import ForrstAPI

fapi = ForrstAPI(use_SSL=False)

stats = fapi.stats()
user = fapi.users_info({'username': 'moopet'})

print str(stats)
print str(user)
