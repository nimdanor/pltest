
# Structure des feedback 

import jinja2

ERROR="error"
FAILURE="failure"
SUCCESS="success"
SYNTAX="syntax"


class OldFeedback:
    def __init__(self, globalok, name, testgroupenum,tests ):
        self.globalok = globalok
        self.name = name
        self.testgroupenum = testgroupenum
        self.tests = tests
    def render(self,filename="template.html"):
        with open(self.filename,"r") as tempfile:
            templatestring = tempfile.read()
        template = jinja2.Template(templatestring)
        x= template.render(feedback=self)
        return  x 

# for type,num,text,got,want in feedback.tests 


class Feedback:
    """
    Classe de gestion du feedback
    contient une liste de feedback pour chaque test TestFeedback
    et pour chaque example ExampleFeedback 
    """
    def __init__(self):
        self.testfeedback = []
        
    def addTestFeedback(self,tfb):
        assert isinstance(tfb,Pltest)
        self.testfeedback.append(TestFeedback(tfb.name))
    @property
    def current(self):
        assert len(self.testfeedback) != 0
        return self.testfeedback[-1]

    def getOutput(self):
        return [x.getOutput() for x in self.testfeedback]

    def jsonStr(self):
        print(self.getOutput())
        return json.dumps(self.getOutput())





class TestFeedback:
    def __init__(self, title="Test exercice"):
        self.title = title
        self.dtests = []

    def addDtest(self,dtest):
        self.dtests.append(dtest)
    def outputdict(self):
        return { "title": self.title, "dtests": [ x.outputdict() for x in self.dtests ] }

    def success(self):
        return all(x.success() for x in self.dtests)
    def buildoldfeedback(self) -> OldFeedback:
        success = self.success()
        return OldFeedback(success," essai ",3,[(1,2,3,4,5)])

class ResultsFeedback:
    def __init__(self, example, succes):
        self.succes = succes
        self.example = example
    def outputdict(self):
        return self.example.outputdict(self.success)



class DtestFeedback:
    def __init__(self, title= None):
        self.title = title if title else "Doc test"
        self.results = []
    def addResults(self, result):
        self.results.append(result)
    def addSuccess(self,example):
        self.results.append(ResultsFeedback(example, True))
    def addEchec(self, example):
        self.results.append(ResultsFeedback(example, False))
    def success(self):
        return all([x.success for x in self.results])

    def outputdict(self):
        return {"title": self.title, "results": [ x.outputdict() for x in self.results ] }

