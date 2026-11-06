import unittest,tempfile,json
from pathlib import Path
from planner import rank_recipes,save,validate,DEFAULT_RECIPES
class PlannerTests(unittest.TestCase):
    def test_ranking_and_missing(self):
        results=rank_recipes([' PASTA ','tomato','olive oil'],DEFAULT_RECIPES)
        self.assertEqual(results[0][:2],('Tomato pasta',[]))
        self.assertEqual(next(r[1] for r in results if r[0]=='Chickpea salad'),['chickpea','cucumber'])
    def test_persistence_and_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'pantry.json';data={'pantry':['egg'],'recipes':DEFAULT_RECIPES};save(path,data)
            self.assertEqual(validate(json.loads(path.read_text())),data)
        with self.assertRaises(ValueError):validate({'pantry':[],'recipes':[{'name':'x','ingredients':[]}]})
if __name__=='__main__':unittest.main()
