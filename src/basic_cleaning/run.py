#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact.
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    logging.info('Downloading data...')
    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)
    logging.info('Done download.')

    logging.info('Cleaning data.')
    # Drop outliers
    min_price = 10
    max_price = 350
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logging.info('Cleaned.')
    # save csv file
    df.to_csv("clean_sample.csv", index=False)

    logging.info('upload cleaned file.')
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="input_artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="output_artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="output_type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Data with outliers and null values removed",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="min price value",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="max price value",
        required=True
    )


    args = parser.parse_args()

    go(args)
