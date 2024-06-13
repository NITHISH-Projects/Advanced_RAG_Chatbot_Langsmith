import os
from langsmith import Client

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__970d62ad405a4415a471223e7ea4e6d9"

#Create dataset for evaluation
dataset_inputs = [
    "How do I subscribe to DDOS from the NWDAF?",
    "What is format of the QoS Sustainability report from the NWDAF?",
    "What is the definition of type Ncgi?",
    "What is the definition of type PlmnId?"
]

# dataset_outputs = [
#     {"must_mention":["DSR", "Topology Hiding"]},
#     {"must_mention":["DSR", "Topology"]},
#     {"must_mention":["Google", "Generative AI"]}
# ]
dataset_outputs = [
    "Suspicion of DDOS Attack is a use case as part of the Abnormal UE Behaviour category defined for the NWDAF.  The subscription method is defined in TS 29.520 section 5.1.6.2.2 and section 5.1.6.2.3.  Attributes that should be set are: supportedFeatures should include AbnormalBehaviour, the event should be set to ABNORMAL_BEHAVIOUR, exptAnaType should be set to COMMUN, and exptAnaType should be set to SUSPICION_OF_DDOS_ATTACK.  The target UEs can be identified by supis, intGroupIds or anyUe attribute in the tgtUe attribute.",
    "The QosSustainabilityInfo type is defined in TS 29.520 section 5.1.6.2.19.  It must contain the areaInfo, startTs, and endTs.  It will conditionally contain the qosFlowRetThd (QoS Flow Retainability Threshold), ranUeThrouThd (RAN UE Throughput Threshold), and snssai.  If it is a prediction, then it will contain the confidence level, which is 0 to 100.  Either qosFlowRetThd or ranUeThrouThd attribute shall be provided.",
    "The type Ncgi is defined in TS 29.571 in section 5.4.4.6 and represents the NR cell identity within an operator’s RAN.  It must contain the PlmnId, NrCellId, and the Nid may be present.  The NID is defined further in TS 23.003.",
    "The type PlmnId is defined in TS 29.571 in section 5.4.4.3 and represents the Mobile Country Code and Mobile Network Code of an operator.  It has the following string pattern: ^[0-9](3)-[0-9]{2,3}$.  Examples are: 262-01 and 302-720."
]

client = Client()
dataset_name = "3gpp_29series_dataset"

dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="3gpp_29series_520_571",
)

client.create_examples(
    inputs=[{"question":q} for q in dataset_inputs],
    outputs=[{"answer":ans} for ans in dataset_outputs],
    dataset_id=dataset.id,
)
