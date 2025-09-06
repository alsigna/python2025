from nornir.core.task import AggregatedResult


def print_summary(result: AggregatedResult) -> None:
    print("SUMMARY:")
    for host, multi_result in result.items():
        failed = any(r.failed for r in multi_result)
        if failed:
            print(f"{host}: ❌ FAILED")
        else:
            print(f"{host}: ✅ OK")
