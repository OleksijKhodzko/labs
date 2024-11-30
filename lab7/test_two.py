from two import SearchTree

def test_comparison():
    a = SearchTree("a")
    b = SearchTree("b")
    assert a.value == "a"
    assert b.value == "b"
    assert a < b
    assert b > a
    assert "a" < b
    assert "b" > a
    assert a < "b"
    assert b > "a"
    assert a == "a"
    c = SearchTree("a")
    assert a == c

def test_sift_down():
    #    q              a
    #    | \            | \
    #    a  b           m  b
    #    | \     ==>    | \ 
    #    z  m           z  q
    #    |              |
    #    c              c
    tree = SearchTree("q",
                      SearchTree("b",
                                 SearchTree("z",
                                            SearchTree("c"),
                                            ),
                                 SearchTree("m"),
                                 ),
                    SearchTree("a"),
                      )
    print("initial")
    print(tree)
    print("-------------")
    tree.sift_down()
    print("Sifted")
    print(tree)
    assert tree == SearchTree("b",
                      SearchTree("m",
                                 SearchTree("z",
                                            SearchTree("c"),
                                            ),
                                 SearchTree("q"),
                                 ),
                    SearchTree("a"),
                      )

def test_sift():
    #    b            b
    #    | \          | \
    #    m  a         c  a
    #    | \    =>    | \
    #    z  q         m  q
    #    |            |
    #    c            z
    tree = SearchTree("b",
                      SearchTree("m",
                                 SearchTree("z",
                                            SearchTree("c"),
                                            ),
                                 SearchTree("q"),
                                 ),
                    SearchTree("a"),
                      )

    print("initial")
    print(tree)
    print("-------------")
    tree.left.left.left.sift_up()
    print("Sifted again")
    print(tree)
    assert tree == SearchTree("b",
                      SearchTree("m",
                                 SearchTree("z",
                                            SearchTree("c"),
                                            ),
                                 SearchTree("q"),
                                 ),
                    SearchTree("a"),
                      )

def test_leaves():
    #    b    
    #    | \  
    #    m  a 
    #    | \  
    #    z  q 
    #    |    
    #    c    
    tree = SearchTree("b",
                      SearchTree("m",
                                 SearchTree("z",
                                            SearchTree("c"),
                                            ),
                                 SearchTree("q"),
                                 ),
                    SearchTree("a"),
                      )
    assert set(tree.leaves) == {SearchTree("a"),
                          SearchTree("q"),
                          SearchTree("c")}

    
