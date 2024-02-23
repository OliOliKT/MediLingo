The folder structure is as follows:

/data
Here I store the raw, unprocessed data

/notebooks
Here I can create notebooks for fast and easy experiment flows - it is not .ipynb notebooks but rather python files with the %## short cuts. If I wished to use .ipynb notebooks it might create import errors.

/saves
Here I store the data preprocessing and models, and maybe samples, I generate and want to save, These are each a different subfolder.

/utils
Here I keep the python scripts that are finally used for the project. They are probabiblt going to be moved from notebooks to here once I have a working plan. It will finally contain code for processing data, building, training, and evaluating models.

Sources:
https://medium.com/analytics-vidhya/how-to-structure-a-machine-learning-project-f190570bd66d

https://medium.com/analytics-vidhya/folder-structure-for-machine-learning-projects-a7e451a8caaa