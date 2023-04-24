# sp23_T2DM_treatment_systems

To run drug_combinations_graph.py, navigate to the repository folder locally and
type the following command in the Terminal/Command Prompt: "python3
drug_combinations_graph.py", should launch to local browser.

# relevant files

Ignore everything except for translate_DDIs.py and drug_combinations_graph.py,
these are the ones you'll need to run

- translate_DDIs.py to process the downloaded csv and turn it into the proper
  format, written out as ddis_from_spreadsheet.csv
- drug_combinations_graph.py which takes in ddis_from_spreadsheet.csv and
  generates the graph

# Modeling DDIs with KG
The knowledge graph shows the relationships between drugs, where nodes are the drugs, color-coordinated by drug class, and edges represent an adverse DDI. That is, the nodes connected by an edge should NOT be taken together. The edges are color-coordinated by classification of risk: mild, moderate, to severe, based on the acuity of the symptoms.

# installing dependencies

pip3 install -r requirements.txt

# using git

Go to your Terminal.

1. git clone "https://git..."
2. git remote-v, should show 2 entries (one for fetch, one for push)
3. git fetch origin main
4. git checkout [name of your branch], you should now be on your branch
5. git pull origin main, will pull from main branch

If you've already cloned and want to commmit,

1. Navigate to the directory where your folder is stored
2. git init
3. git checkout [branch name]
4. Follow steps 3-5 above, then steps 1-3 below

When you're ready to commit your changes,

1. git add .
2. git commit -m "message about your commit"
3. git push, this will push to your branch.

When you want to edit on your branch but first have to pull from main:
1. Create a pull request in GitHub, [branch] <-- main.
2. git fetch
3. git pull

Then, go to the browser and click on "new pull request", assign reviewers if
needed
