import utilits

# Testando a quantidade de generos que foram resgatados
def unit_test():
    links = utilits.gerador_links()
    assert len(links) == 27

unit_test()
    
