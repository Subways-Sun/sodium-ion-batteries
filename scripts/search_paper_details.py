from sib.literature.semantic import search_paper_details as spd

out = spd("10.1021/acsami.7b05687", fields = "title,authors,year")
print(out)