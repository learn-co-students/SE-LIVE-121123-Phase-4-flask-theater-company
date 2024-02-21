#!/usr/bin/env python3
import ipdb
from app import app
from models import Production, db

# This debug file can be used in place of flask shell
if __name__ == "__main__":
    with app.app_context():

        productions = Production.query.all()
        p1 = Production.query.first()

    ipdb.set_trace()
