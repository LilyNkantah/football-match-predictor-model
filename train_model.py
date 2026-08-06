import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings

from model_data import build_training_data
import database

"""
Responsibilities of this file:
1. Retrieve the finished dataset containing the necessary features
2. Splitting the dataset into the TSCV (Time Series Cross-Validation) folds for training and testing
3. Fitting a RandomForestClassifier model (using the training sets)
4. Evaluating the model (using the testing set)
5. Repeat this fitting and evaluating on each fold
- I will use 2 folds: (Train: 1 / Test: 2), (Train: 1+2 / Test: 3) 
"""

warnings.filterwarnings("ignore")

DATABASE_URL = (
    "sqlite:///./football_predictor.db"  # SQLite database URL for local development
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


def build_model(preds, X_train, y_train, X_test, y_test):
    """Train a Random Forest on one TSCV fold, evaluate it, and append its test-set predictions (with fixture data) to preds."""
    # use the split data to train Random Forest model
    rf_classifier = RandomForestClassifier(n_estimators=99, random_state=None)
    rf_classifier.fit(X_train, y_train)

    X_pred_test = [row[2:] for row in X_test]  # extract features for testing

    # predict on test data
    y_pred = rf_classifier.predict(X_pred_test)

    # add predictions to the database
    for test_row, fix, pred in zip(X_test, X_pred_test, y_pred):
        fixture_id = test_row[0]
        preds.append(
            (fixture_id, *fix, pred.item())
        )  # append fixture_id, features, and prediction for each fixture

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

    # add prediction data to the database
    predictions = []

    # TSCV - Fold 1
    # Training (season 1)
    X1_train = [row[2:-1] for row in feature_rows if row[1] == 1]
    y1 = [row[-1] for row in feature_rows if row[1] == 1]

    # add predictions data for season 1 fixtures
    predictions = [row[0:-1] + (None,) for row in feature_rows if row[1] == 1]
    # remove season_id from predictions data
    predictions = [row[0:1] + row[2:] for row in predictions]

    # Testing (season 2)
    X2_test = [row[:-1] for row in feature_rows if row[1] == 2]
    y2 = [row[-1] for row in feature_rows if row[1] == 2]

    # TSCV - Fold 2
    # Training (season 1 + season 2)
    X2_train = [row[2:-1] for row in feature_rows if row[1] == 2]
    X1_2_train = X1_train + X2_train
    y1_2 = y1 + y2

    # Testing (season 3)
    X3_test = [row[:-1] for row in feature_rows if row[1] == 3]
    y3 = [row[-1] for row in feature_rows if row[1] == 3]

    fold1_pred = build_model(predictions, X1_train, y1, X2_test, y2)
    fold2_pred = build_model(predictions, X1_2_train, y1_2, X3_test, y3)

    database.add_predictions_to_db(db, predictions)
