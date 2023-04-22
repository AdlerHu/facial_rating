# facial_rating

Using AI for facial rating.

1. Download SCUT-FBP5500_v2 dataset and unzip it to dataset/

2. Calculate average score by database
    - Create required tables
        - facial_rating.sql
    - Load All_Ratings.csv into database
    - Calculate average score and insert

3. Create a porgram to connect db
    - utils/config.py

4. data preprocessing
    - prepare_data.py

5. Train and verify model
    - train_model.py
    - verify.py

6. A simple web page renders
    - webapp.py

7. Prepare multiple photos of yourself in my_face/

8. Deciding your own style
    - my_face_rating.py