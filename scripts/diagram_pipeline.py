"""데이터 파이프라인 아키텍처 다이어그램.

데이터 파이프라인 설계·도입(2022.07-2023.03) 프로젝트의
최종 아키텍처를 시각화한다. 4곳에 분산된 인프라 구조를 보여준다.
"""

import os

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.workflow import Airflow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(BASE_DIR, "..", "images", "aws-icons")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "images")

# 아이콘 경로
IC_RDS = os.path.join(ICONS, "Databases", "Arch_Amazon-RDS_64.png")
IC_GLUE = os.path.join(ICONS, "Analytics", "Arch_AWS-Glue_64.png")
IC_EC2 = os.path.join(ICONS, "Compute", "Arch_Amazon-EC2_64.png")
IC_S3 = os.path.join(ICONS, "Storage", "Arch_Amazon-Simple-Storage-Service_64.png")
IC_ATHENA = os.path.join(ICONS, "Analytics", "Arch_Amazon-Athena_64.png")
IC_REDASH = os.path.join(BASE_DIR, "..", "images", "third-party", "redash.png")

with Diagram(
    "",
    filename=os.path.join(OUTPUT_DIR, "data-pipeline"),
    show=False,
    direction="LR",
    outformat="png",
    graph_attr={
        "bgcolor": "transparent",
        "pad": "0.5",
        "fontcolor": "#e6edf3",
    },
    node_attr={"fontcolor": "#e6edf3"},
    edge_attr={"color": "#4ade80", "fontcolor": "#8b949e"},
):
    mysql = Custom("MySQL\nService DB", IC_RDS)

    with Cluster("ETL (4곳 분산)", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        glue = Custom("Glue\n대부분 테이블", IC_GLUE)
        mac = Custom("Mac Studio\n대용량 테이블", IC_EC2)
        ec2 = Custom("EC2\n가공 스크립트", IC_EC2)

    with Cluster("Storage", graph_attr={"bgcolor": "#161b22", "fontcolor": "#8b949e"}):
        s3 = Custom("S3\nraw / core / output", IC_S3)

    catalog = Custom("Glue\nData Catalog", IC_GLUE)
    athena = Custom("Athena", IC_ATHENA)
    redash = Custom("Redash", IC_REDASH)
    users = User("전사 사용자")

    mysql >> Edge(label="Spark") >> glue >> s3
    mysql >> Edge(label="pandas") >> mac >> s3
    mysql >> Edge(label="Python") >> ec2 >> s3

    s3 >> catalog >> athena >> redash >> users
