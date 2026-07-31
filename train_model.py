import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings

from model_data import build_training_data

"""
Responsibilities of this file:
1. Retrieve the finished dataset containing the necessary features
2. Splitting the dataset into the TSCV (Time Series Cross-Validation) folds for training and testing
3. Fitting a RandomForestClassifier model (using the training sets)
4. Evaluating the model (using the testing set)
5. Repeat this fitting and evaluating on each fold
- I will use 2 folds: (Train: 1 / Test: 2), (Train: 1+2 / Test: 3) 
"""

warnings.filterwarnings('ignore')

DATABASE_URL = "sqlite:///./football_predictor.db"  # SQLite database URL for local development
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

def build_model(X_train, y_train, X_test, y_test):
    # use the split data to train Random Forest model
    rf_classifier = RandomForestClassifier(n_estimators=99, random_state=None)
    rf_classifier.fit(X_train, y_train)

    # predict on test data
    y_pred = rf_classifier.predict(X_test)

    # check accuracy of prediction
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.2f}") 
    print("\nClassification Report:\n", classification_rep)

    return y_pred

if __name__ == "__main__":
    db = SessionLocal()
    try:
        feature_rows = build_training_data(db)
    finally:
        db.close()

    # TSCV - Fold 1
    # training X (features) and y (outcome) - season 1
    X1 = [row[2:-1] for row in feature_rows if row[1] == 1]
    y1 = [row[-1] for row in feature_rows if row[1] == 1]
    # testing X and y - season 2
    X2 = [row[2:-1] for row in feature_rows if row[1] == 2]
    y2 = [row[-1] for row in feature_rows if row[1] == 2]

    # TSCV - Fold 2
    # training X and y - season 1+2
    X1_2 = X1 + X2
    y1_2 = y1 + y2 
    # testing X and y - season 3
    X3 = [row[2:-1] for row in feature_rows if row[1] == 3]
    y3 = [row[-1] for row in feature_rows if row[1] == 3]

    fold1_pred = build_model(X1, y1, X2, y2)

    fold2_pred = build_model(X1_2, y1_2, X3, y3)
