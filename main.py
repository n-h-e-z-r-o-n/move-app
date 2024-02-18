import movieposters as mp
link = mp.get_poster(title='breakfast club')
assert link == mp.get_poster(id='tt0088847')  # can also be found using movie's id
assert link == mp.get_poster(id=385687)
assert link == 'https://m.media-amazon.com/images/M/MV5BOTM5N2ZmZTMtNjlmOS00YzlkLTk3YjEtNTU1ZmQ5OTdhODZhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_QL75_UX380_CR0,16,380,562_.jpg'