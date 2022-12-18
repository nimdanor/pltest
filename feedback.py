
# Structure des feedback 

#https://www.plantuml.com/plantuml/png/RSr12i8m48NX_PoYTAMB5ho0TADUm0kawKF4J58o4nIaTtSM4gGsop3l-mTHbxLm87i-E97cz78y1vo1QNJ-qRp9RXJqT57fbfJqhW6xFVd43FjRw0hHIqvbhgEkEpRjeUzZk_Q-bV-9TOht434w5XwHQsaXsf9NHhKtoHzhG9mAXmy0

import json
import jinja2

import pltest

ERROR="error"
FAILURE="failure"
SUCCESS="success"
SYNTAX="syntax"
EXCEPTION= "exception"
states = [ERROR, FAILURE, SUCCESS,SYNTAX,EXCEPTION]

class OldFeedback:
    def __init__(self, globalok, name, testgroupenum,tests ):
        self.globalok = globalok
        self.name = name
        self.testgroupenum = testgroupenum
        self.tests = tests
        self.filename = "template.html"
        
    def __render(self,filename=None):
        if filename:
            self.filename = filename        
        with open(self.filename,"r") as tempfile:
            templatestring = tempfile.read()
        template = jinja2.Template(templatestring)
        x= template.render(feedback=self)
        return  x 


# for type,num,text,got,want in feedback.tests 




class ExampleFeedback:
    def __init__(self,success, mode,title,want,got=None):
        self.success = success
        assert mode in states
        self.mode = mode
        self.title = title
        self.want = want
        if not got:
            self.got = want
        else:
            self.got = got
        
    def todic(self):
        return {"success": self.mode, "title": self.title, "got": self.got, "want":self.want}

    def getOutput(self):
        return self.todic()

    def success(self):
        return self.success 


class TestFeedback:
    def __init__(self, title="Test exercice"):
        self.title = title
        self.efeedback = []

    def getOutput(self):
        return [ x.getOutput() for x in self.efeedback]


    def append(self,efb:ExampleFeedback):
        self.efeedback.append(efb)
        
    def outputdict(self):
        return { "title": self.title, "dtests": [ x.outputdict() for x in self.efeedback ] }

    @property
    def success(self):
        return all([x.success for x in self.efeedback])

    
    def buildoldfeedback(self):
        return [OldFeedback(self.title,self.success,42,self.efeedback)]


class Feedback:
    """
    Classe de gestion du feedback
    contient une liste de feedback pour chaque test TestFeedback
    et pour chaque example ExampleFeedback 
    """
    def __init__(self):
        self.testfeedback = []
        
    def addTestFeedback(self,tfb):
        assert isinstance(tfb,pltest.Pltest)
        newtfeedback =TestFeedback(tfb.name)
        self.testfeedback.append(newtfeedback)
        return newtfeedback
    
    @property
    def current(self):
        assert len(self.testfeedback) != 0
        return self.testfeedback[-1]

    def getOutput(self):
        return [x.getOutput() for x in self.testfeedback]

    @property
    def success(self):
        return all(x.success for x in self.testfeedback)

    def jsonStr(self):
        print(self.getOutput())
        return json.dumps(self.getOutput())
    
    def buildoldfeedback(self) -> OldFeedback:
        success = self.success
        return OldFeedback(success," essai ",3,[x.buildoldfeedback() for x in self.testfeedback])

