from __future__ import annotations

from .utils import call_dequeue, call_enqueue, call_size, iso_ts, run_queue


def test_enqueue_size_dequeue_flow() -> None:
    run_queue([
        call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
        call_size().expect(1),
        call_dequeue().expect("companies_house", 1),
    ])
    print("test_enqueue_size_dequeue_flow")

def test_rule_of_three_dequeue_single_flow() -> None:
    run_queue([
        call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
        call_enqueue("bank_statements", 2, iso_ts(delta_minutes=0)).expect(2),
        call_enqueue("id_verification", 1, iso_ts(delta_minutes=0)).expect(3),
        call_enqueue("bank_statements", 1, iso_ts(delta_minutes=0)).expect(4),
        call_size().expect(4),
        call_dequeue().expect("companies_house", 1),
        call_size().expect(3),
    ])
    print("test_rule_of_three_dequeue_single_flow")

def test_rule_of_three_dequeue_multiple_flow() -> None:
    run_queue([
        call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
        call_enqueue("bank_statements", 2, iso_ts(delta_minutes=0)).expect(2),
        call_enqueue("id_verification", 1, iso_ts(delta_minutes=0)).expect(3),
        call_enqueue("bank_statements", 1, iso_ts(delta_minutes=0)).expect(4),
        call_size().expect(4),
        call_dequeue().expect("companies_house", 1),
        call_dequeue().expect("id_verification", 1),
        call_size().expect(2),
    ])
    print("test_rule_of_three_dequeue_multiple_flow")

def test_rule_of_three_dequeue_all_flow() -> None:
    run_queue([
        call_enqueue("companies_house", 1, iso_ts(delta_minutes=0)).expect(1),
        call_enqueue("bank_statements", 2, iso_ts(delta_minutes=0)).expect(2),
        call_enqueue("id_verification", 1, iso_ts(delta_minutes=0)).expect(3),
        call_enqueue("bank_statements", 1, iso_ts(delta_minutes=0)).expect(4),
        call_size().expect(4),
        call_dequeue().expect("companies_house", 1),
        call_dequeue().expect("id_verification", 1),
        call_dequeue().expect("bank_statements", 1),
        call_dequeue().expect("bank_statements", 2),
        call_size().expect(0),
    ])
    print("test_rule_of_three_dequeue_all_flow")

def test_timestamp_ordering_dequeue_older_flow() -> None:
    run_queue([
        call_enqueue("bank_statements", 1, iso_ts(delta_minutes=5)).expect(1),
        call_enqueue("bank_statements", 2, iso_ts(delta_minutes=0)).expect(2),
        call_size().expect(2),
        call_dequeue().expect("bank_statements", 2),
        call_dequeue().expect("bank_statements", 1),
    ])
    print("test_timestamp_ordering_dequeue_older_flow")

def test_dependency_resolution_added_dependencies_flow() -> None:
    run_queue([
        call_enqueue("credit_check", 1, iso_ts(delta_minutes=0)).expect(2),
        call_size().expect(2),
        call_dequeue().expect("companies_house", 1),
        call_dequeue().expect("credit_check", 1),
    ])

def test_resolve_deduplication_dlow() -> None:
    run_queue([
        call_enqueue("bank_statements", 1, iso_ts(delta_minutes=5)).expect(1),
        call_enqueue("bank_statements", 1, iso_ts(delta_minutes=0)).expect(1),
        call_enqueue("id_verification", 1, iso_ts(delta_minutes=5)).expect(2),
        call_size().expect(2),
        call_dequeue().expect("bank_statements", 1),
        call_dequeue().expect("id_verification", 1),
        call_size().expect(0),
    ])