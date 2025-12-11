import argparse
import json
from arxiv_tool import arxiv_search


def main():
	parser = argparse.ArgumentParser(description="AI Researcher Agent: arXiv search")
	parser.add_argument("topic", help="Topic to search on arXiv, e.g. 'large language models'")
	parser.add_argument("--max-results", type=int, default=5, dest="max_results", help="Maximum number of results")
	args = parser.parse_args()

	# Run the tool and pretty-print results
	result = arxiv_search.invoke(args.topic)
	entries = result.get("entries", [])
	if args.max_results and len(entries) > args.max_results:
		entries = entries[: args.max_results]

	print(json.dumps(entries, indent=2, ensure_ascii=False))


if __name__ == "__main__":
	main()

