import pandas as pd

df = pd.read_csv('Diabetes_Drug-Drug_Interactions.csv')
df = df.rename({"Drug": "Source", "Not Advised With (Specific Drug, no need to list drugs if they belong to a class that's in the previous column)": "Single Drug",
               "Not Advised With (Class of Drug, put SINGULAR!)": "Adverse Class"}, axis=1)

"""First write out straightforward source - target - label triplets"""
df_singles = df[df['Single Drug'].notna()]  # slice dataframe to just see
# need to map from "Adverse Class" to "Class" column and fetch those drugs
df_singles = df_singles[['Source', 'Single Drug', 'Classification of Risk']]
df_singles = df_singles.rename(
    {"Source": 'source', 'Single Drug': 'target', 'Classification of Risk': 'label'}, axis=1)
df_singles.to_csv('./ddis_from_spreadsheet.csv', index=False)


def add_list(drug_class, drug_class_mappings):
    try:
        return drug_class_mappings[drug_class]
    except:
        return None


"""1. Look for individual drugs that have an Adverse Class"""
drugs_with_adverse_class = df[df['Adverse Class'].notna()]

"""2. Get mapping of class:drugs in that class"""
classes = set(df['Class'])
# need to get the union of adverse classes and regular classes
adv_classes = set(df['Adverse Class'])
classes = classes.union(adv_classes)

class_mapping = {}
for class_ in classes:
    drugs_in_class = set(df[df['Class'] == class_]['Source'])
    class_mapping[class_] = drugs_in_class
# print(class_mapping)

"""2. For every drug with an Adverse Class, find the drugs that correspond to that class and create edges."""
df_new = df.copy()
df_new['Drugs in Adverse Class'] = drugs_with_adverse_class['Adverse Class'].apply(
    add_list, drug_class_mappings=class_mapping)
df_new = df_new.explode('Drugs in Adverse Class')
df_classes_slice = df_new[[
    'Source', 'Drugs in Adverse Class', 'Classification of Risk']]

# now remove triples with no Single Drug
df_classes_rm = df_classes_slice.dropna(subset=['Drugs in Adverse Class'])
df_classes_rm.to_csv('./ddis_from_spreadsheet.csv',
                     mode='a', header=False, index=False)
