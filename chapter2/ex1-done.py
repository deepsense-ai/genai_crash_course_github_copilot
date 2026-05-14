"""Plot 7-day forecast temperatures for a selected location.

Example:
	python chapter2/ex1-done.py --capital warsaw --output chapter2/forecast_warsaw.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import httpx
import matplotlib

# Headless-friendly backend for scripts.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CAPITALS: dict[str, tuple[str, float, float]] = {
	"london": ("London", -0.1278, 51.5074),
	"paris": ("Paris", 2.3522, 48.8566),
	"berlin": ("Berlin", 13.4050, 52.5200),
	"madrid": ("Madrid", -3.7038, 40.4168),
	"rome": ("Rome", 12.4964, 41.9028),
	"warsaw": ("Warsaw", 21.0122, 52.2297),
	"prague": ("Prague", 14.4378, 50.0755),
	"vienna": ("Vienna", 16.3738, 48.2082),
	"lisbon": ("Lisbon", -9.1393, 38.7223),
	"stockholm": ("Stockholm", 18.0686, 59.3293),
}


def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments for the forecast script.

	Returns:
		argparse.Namespace: Parsed arguments containing capital, lat, lon, output,
			and list_capitals options.
	"""
	parser = argparse.ArgumentParser(
		description="Fetch 7-day forecast and save a temperature plot image."
	)
	parser.add_argument(
		"--capital",
		default="warsaw",
		choices=sorted(CAPITALS.keys()),
		help="Predefined European capital to use.",
	)
	parser.add_argument(
		"--lat",
		type=float,
		help="Latitude override. Must be used together with --lon.",
	)
	parser.add_argument(
		"--lon",
		type=float,
		help="Longitude override. Must be used together with --lat.",
	)
	parser.add_argument(
		"--output",
		default="forecast.png",
		help="Output image path, e.g. chapter2/forecast.png",
	)
	parser.add_argument(
		"--list-capitals",
		action="store_true",
		help="Print available capital options and exit.",
	)
	return parser.parse_args()


def resolve_location(args: argparse.Namespace) -> tuple[str, float, float]:
	"""Resolve the location coordinates from parsed arguments.

	Args:
		args: Parsed command-line arguments.

	Returns:
		tuple[str, float, float]: A tuple of (location_name, longitude, latitude).

	Raises:
		ValueError: If latitude/longitude are provided without both, or if
			coordinates are outside valid ranges.
	"""
	if (args.lat is None) ^ (args.lon is None):
		raise ValueError("Please provide both --lat and --lon together.")

	if args.lat is not None and args.lon is not None:
		if not -90 <= args.lat <= 90:
			raise ValueError("Latitude must be between -90 and 90.")
		if not -180 <= args.lon <= 180:
			raise ValueError("Longitude must be between -180 and 180.")
		return "Custom location", args.lon, args.lat

	city_name, lon, lat = CAPITALS[args.capital]
	return city_name, lon, lat


def fetch_forecast(lat: float, lon: float) -> tuple[list[str], list[float], list[float]]:
	"""Fetch 7-day weather forecast from Open-Meteo API.

	Args:
		lat: Latitude of the location.
		lon: Longitude of the location.

	Returns:
		tuple[list[str], list[float], list[float]]: A tuple of (dates, max_temps, min_temps)
			where dates are ISO format strings and temperatures are in Celsius.

	Raises:
		ValueError: If the API response is missing expected fields or has mismatched
			series lengths.
		httpx.HTTPError: If the API request fails.
	"""
	response = httpx.get(
		"https://api.open-meteo.com/v1/forecast",
		params={
			"latitude": lat,
			"longitude": lon,
			"daily": "temperature_2m_max,temperature_2m_min",
			"forecast_days": 7,
			"timezone": "auto",
		},
		timeout=15.0,
	)
	response.raise_for_status()
	payload = response.json()

	daily = payload.get("daily", {})
	dates = daily.get("time")
	t_max = daily.get("temperature_2m_max")
	t_min = daily.get("temperature_2m_min")

	if not dates or not t_max or not t_min:
		raise ValueError("Weather API response is missing expected daily temperature fields.")
	if not (len(dates) == len(t_max) == len(t_min)):
		raise ValueError("Weather API response contains mismatched daily series lengths.")

	return dates, t_max, t_min


def plot_temperatures(
	dates: list[str], t_max: list[float], t_min: list[float], location: str, output_path: Path
) -> None:
	"""Create and save a temperature forecast plot.

	Args:
		dates: List of date strings in ISO format.
		t_max: List of maximum temperatures in Celsius.
		t_min: List of minimum temperatures in Celsius.
		location: Name of the location for the plot title.
		output_path: Path where the plot image will be saved.
	"""
	fig, ax = plt.subplots(figsize=(10, 5))
	ax.plot(dates, t_max, marker="o", label="Max temperature (°C)")
	ax.plot(dates, t_min, marker="o", label="Min temperature (°C)")

	ax.set_title(f"7-day forecast for {location}")
	ax.set_xlabel("Date")
	ax.set_ylabel("Temperature (°C)")
	ax.grid(alpha=0.3)
	ax.legend()
	plt.xticks(rotation=30, ha="right")
	fig.tight_layout()

	output_path.parent.mkdir(parents=True, exist_ok=True)
	fig.savefig(output_path, dpi=160)
	plt.close(fig)


def print_capitals() -> None:
	"""Print all available European capitals with their coordinates."""
	print("Available capitals (key -> City [lon, lat]):")
	for key, (city, lon, lat) in sorted(CAPITALS.items()):
		print(f"- {key:10s} -> {city} [{lon},{lat}]")


def main() -> int:
	"""Main entry point for the forecast script.

	Returns:
		int: Exit code (0 for success, 1 for error).
	"""
	args = parse_args()

	if args.list_capitals:
		print_capitals()
		return 0

	try:
		location_name, lon, lat = resolve_location(args)
		dates, t_max, t_min = fetch_forecast(lat=lat, lon=lon)
		output_path = Path(args.output)
		plot_temperatures(dates, t_max, t_min, location_name, output_path)

		print(f"Location: {location_name} (lon={lon}, lat={lat})")
		print(f"Saved plot: {output_path.resolve()}")
		return 0
	except (ValueError, httpx.HTTPError) as exc:
		print(f"Error: {exc}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	raise SystemExit(main())

