
def build(objects):
    repo = objects["repositories"][0]
    #repo.clone()
    package = objects["packages"][0]
    package.build(repo)
    return objects
