
import doctest 

import testingdoctest

if __name__ == "__main__":
    # testing test classes
    import sys
    import pltest

    tester = pltest.PlRunner(open("student.py","r").read(),">>> f(6)\n6\n>>> f( 5)\n5\n>>> f(4)\n4\n")
    tester.addPltest(">>> f(6)\n6\n>>> f( 5)\n4\n>>> f(4/0)\n4\n","Nom 1")
        
    tester.addPltest("""
                        >>> f(6)#
                        6
                        >>> f(5)##
                        5
                        >>> f(5)# Un test
                        5
                        >>> f(7)# Hidden with an indication in case of failure must end with ->#
                        7""","Nom bizaroide")
    a, f = tester.runpltest("oh le test")

    print(f"grade : {a} feedback:")

    print(f.jsonStr(), file=open("result.json","w"))    

    pltest.printOutput(f.getOutput())
    
    print(f.buildoldfeedback())