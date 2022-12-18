



# Version 26/9/2019
# ajout de runcompiletest 
import doctest
import traceback 
import json
from doctest import DocTest

from feedback import TestFeedback, ExampleFeedback,Feedback


#debug to be removed
import sys


def printOutput(o):
    for t in o:
        print("----------------------------------------------------------------")
        print(t["title"])
        if t["success"] == True: 
            print("++++++++++++++++++++++++++++++++++++++++++++++++")
        else:
            print("------------------------------------------------")
        
        for x in t["tests"]:
            print("titre:", x["title"])
            if x["success"] == True :
                print("bravo :\n",x["got"])
            else: 
                if x["want"] != None:
                    print("echec :\n attendu : \n",x["want"],"optenu:\n",x["got"])
                else:
                    print("echec:\n",x["got"])

class PlExample:
    @classmethod
    def __exampleType(cls,example: doctest.Example):
        """
        Défini le type de sortie en fonction de la ligne de commentaire qui suis la ligne de source
        
        Si pas de commentaire le type est 'standard'
        Si le commentaire est réduit a des caractères 'whites' alors le type est 'Hidden'
        Sinon si le commentaire Commence par le caractère # le type 'Caviar' 
        Sinon le type est 'Nospoiler' 
        
            
        """
        assert  isinstance(example,doctest.Example)
        line = example.source[:] if not example.source.endswith("\n") else example.source[:-1]
        
        example.title = line
        
        if "#" not in line:
            example.__class__ = Standard
        else:

            if line.endswith("#"): # Hidden
                example.__class__ = Hidden 
                # titre = source, ce qui ne fonctionne pas 
                example.title = line[:-1] # moins le # 
            else:
                found = line.split("#", 1) # couper sur le premier #
                if found[1].startswith("#"): #  Caviar
                    example.__class__ = Caviar
                    example.caviar = found[1][1:]
                    example.title = example.caviar
                    # titre = source 
                else:
                    example.__class__ = Nospoiler # caviar automatique 
                    example.title = found[1][1:] # le commentaire remplace le contenu du test
        assert example.__class__ in [ Caviar, Hidden,Standard, Nospoiler]

    @classmethod
    def update(cls,example: doctest.Example, name, mode):
        # inplace cast of Exemple in Standard/Hidden/...
        cls.__exampleType(example)
        example.name = name
        example.mode = mode

from feedback import SUCCESS,FAILURE,ERROR,EXCEPTION

class Standard(doctest.Example):

    def addSucess(self, feedback:TestFeedback,  got):
        feedback.append(ExampleFeedback(True,SUCCESS, self.title,self.want))

    def addFailure(self, feedback:TestFeedback, got):
        feedback.append(ExampleFeedback(False,FAILURE, self.title,self.want,got))
        
    def addException(self, feedback:TestFeedback, infos):
        feedback.append(ExampleFeedback(False,EXCEPTION, "le copain",None,infos))
        

class Hidden(Standard):
    def addSucess(self, feedback:TestFeedback,  got):
        # feedback.append(ExampleFeedback(True, self.title,self.want,got))
        pass # no feedback it's good

    def addFailure(self, feedback:TestFeedback, got):
        # pas de want et un got -> le problem
        feedback.append(ExampleFeedback(False, self.title,None,got))


class Caviar(Standard):
    def addSucess(self, feedback:TestFeedback,  got):
        feedback.append(ExampleFeedback(True, self.title,self.want,self.caviar))

    def addFailure(self, feedback:TestFeedback, got):
        feedback.append(ExampleFeedback(False, self.title,self.want,self.caviar))
        

class Nospoiler(Standard):
    pass






class Pltest(DocTest):
    STOPONFIRSTFAIL = 1
    
    def __init__(self, theTest:DocTest):
        super(Pltest, self).__init__(*theTest)        

    @classmethod
    def cast(cls, dt: DocTest, name,mode):
        """Cast an Doctest into Pltest."""
        assert isinstance(dt, DocTest)
        dt.__class__ = cls  # now mymethod() is available
        dt.name = name
        dt.mode = mode
        for i,e in enumerate(dt.examples):
            PlExample.update(e,f"{name}-{i}",mode)
        return dt

        
        
        
class PlRunner(doctest.DocTestRunner):
    def __init__(self,studentcode,optionflags= doctest.NORMALIZE_WHITESPACE):
        self.optionflags= doctest.NORMALIZE_WHITESPACE
        self.right = 0
        self.fail = 0
        self.total = 0
        self.testnum = -1
        self.student= studentcode
        self.points = 0
        super().__init__(verbose=True)
        self.pltests = []
        self.feedback =  Feedback()
    
    def addPltest(self,pltest,name=None, mode= 0):
        if not name:
            name = "Test °{len(self.pltests)+1}"
        self.pltests.append({"test":pltest,"name":name,"mode":mode})
        
    
    def runpltest(self,title=None):

            dic = {}
            # dic['__student']=self.student
            try:
                compile(self.student,"Votre code",'exec')
                print("compile ok")
                exec(self.student, dic)
                print("exec ok")
            except SyntaxError as e:
                print("Syntaxe error")
            except Exception as e:
                print("exception")    
            else:
                for t in self.pltests:
                    pltest = t["test"] 
                    # attention la fonction run
                    # doit être lancé juste après le get_doctest
                    # et une seule fois car le source stoké est libéré à la fin de run
                    test = doctest.DocTestParser().get_doctest(pltest, dic, 'votre travail', 'foo.py', 0)
                    Pltest.cast(test,t["name"],0) # biensur il faut transformer
                    # les test et les examples
                    self.feedback.addTestFeedback(test)
                    self.run(test)

            return self.grade(),self.feedback

    def getFeedback(self):
        self.feedback.getOutput()
        return self.feedback.getOutput()
 
    def runcompiletest(self, dic={}, name="compiletest"):
        try:
            compile(self.student,"Votre code",'exec')
            exec(self.student, dic)
            return True,"Compilation OK"
        except SyntaxError as e:
            print("Syntaxe error")
        except Exception as e:
            print("exception")    
        else:
            pass
        return False," feedback compile pas ok"

            
            
 
    def report_start(self, out, test, example):
        print("starting ",example.name, file=sys.stderr)

    def report_success(self, out, test, example, got):
        example.addSucess(self.feedback.current, got)
        
    def report_failure(self, out, test, example, got):
        example.addFailure(self.feedback.current, got)

    def report_unexpected_exception(self, out, test, example, exc_info ):
        # (type(e), e, e.__traceback__)
        text= f"Exception {exc_info[1]}"# {exc_info[2].format_exception()}"
        example.addException(self.feedback.current, text)
        
    def summarize(self):
        print("résumé", file=sys.stderr)
        
    def grade(self):
        return self.points








