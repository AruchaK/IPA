import pytest
from textfsmlab import generate_interface_descriptions, get_cdp_from_device

def test_r1_description():
    output = get_cdp_from_device("172.31.36.4")
    expected = {
        "Gig 0/0": "Connect to Gig 0/1 of S0.ipa.com",
        "Gi0/1": "Connect to PC",
        "Gig 0/2": "Connect to Gig 0/1 of R2.ipa.com",
    }
    assert generate_interface_descriptions(output, "172.31.36.4") == expected

def test_r2_description():
    output = get_cdp_from_device("172.31.36.5")
    expected = {
        "Gig 0/0": "Connect to Gig 0/2 of S0.ipa.com",
        "Gig 0/1": "Connect to Gig 0/2 of R1.ipa.com",
        "Gig 0/2": "Connect to Gig 0/1 of S1.ipa.com",
        "Gi0/3": "Connect to WAN",
    }
    assert generate_interface_descriptions(output, "172.31.36.5") == expected

def test_s1_description():
    output = get_cdp_from_device("172.31.36.3")
    expected = {
        "Gig 0/0": "Connect to Gig 0/3 of S0.ipa.com",
        "Gig 0/1": "Connect to Gig 0/2 of R2.ipa.com",
        "Gi1/1": "Connect to PC",
    }
    assert generate_interface_descriptions(output, "172.31.36.3") == expected
