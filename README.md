# Smart Bus Ticket Booking & Reservation System

A text-based Python 3 application for a small bus service. Browse routes, search journeys,
book seats, cancel bookings, check availability, view schedules and generate reports, all from a console menu.

> **Core rule of the program: validate first, change state second.**
> Seat counts and booking records are only modified after every check has passed.

## Requirements
- Python 3.8 or newer
- No external libraries (built-in Python only)

## How to run
```bash
python main.py
```
(Use `python3 main.py` on macOS/Linux if `python` points to Python 2.)

## Menu guide
| Option | What it does |
|---|---|
| 1. View Available Routes | Lists all routes with fare and seats (`available/total`, or *Fully Booked*). Optional "only routes with seats" filter. |
| 2. Search for a Route | Search by route ID or by departure/destination city (case-insensitive). |
| 3. Book a Ticket | Asks for name, age, route ID and seats; validates; calculates fare; issues a unique booking ID. |
| 4. View My Bookings | Lists every booking, including cancelled ones. |
| 5. Cancel a Booking | Cancels a *Confirmed* booking by ID and restores its seats exactly once. |
| 6. View Seat Availability | Sub-menu: all routes with status, only routes with seats, or the **route schedule by departure city**. |
| 7. Generate Booking Report | Totals, reserved seats, confirmed revenue, fully booked routes, plus a per-route breakdown. |
| 8. Exit | Ends the program. |

**Design note:** the PRD describes a Route Schedule feature (Feature 10) but gives it no menu number
within the 8-option menu. It is placed as sub-option 3 under *6. View Seat Availability*, so the
required menu stays exactly as specified.

## Sample workflow
1. Choose `1` to see the five routes.
2. Choose `2` and type `hyderabad` to see routes departing from or arriving at Hyderabad.
3. Choose `3`: name `Ahmed`, age `24`, route `R101`, seats `2` -> booking `B1001`, total Rs. 2400. R101 drops from 40 to 38 seats.
4. Choose `5` and enter `B1001` -> booking cancelled, 2 seats restored (R101 back to 40).
5. Choose `5` and enter `B1001` again -> rejected, no extra seats restored.
6. Choose `7` -> the report excludes the cancelled booking from revenue.

## Data structures and why
| Structure | Used for | Why |
|---|---|---|
| `list` of `dict` | `routes`, `bookings` | Ordered collections of records with named fields |
| `tuple` | `CITIES` | The supported cities never change |
| `set` | `issued_ids` | Fast membership check guarantees unique booking IDs |
| `dict` | each route / booking | Keeps related fields together |

## Business rules enforced
- Name must not be blank; age must be a whole number from 1 to 120; seats must be a whole number > 0.
- Route must exist; requested seats must not exceed available seats.
- Total fare = ticket price x seats.
- Booking IDs are unique (`B1001`, `B1002`, ...).
- Only *Confirmed* bookings can be cancelled; cancelled records are kept for history.
- Seats are restored once per cancellation. `0 <= available_seats <= total_seats` always holds.
- Revenue and reserved seats count *Confirmed* bookings only.

## Limitations (please read)
- **Storage is in memory only.** All routes, bookings and booking IDs are lost when the program closes.
  Every run starts fresh with the five sample routes.
- Single console user; no login or roles.
- No payment, database, GUI or network features (out of scope per the PRD).

## Project files
- `main.py` - the complete program
- `README.md` - this file
- `test_cases.txt` - the 12 required test scenarios with expected and actual results
