CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad",
     "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur",
     "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas",
     "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore",
     "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad",
     "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30},
]

bookings = []
issued_ids = set()
next_booking_number = 1001

MAX_AGE = 120


def get_number(question):
    text = input(question).strip()
    if "_" in text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def find_route(route_id):
    for route in routes:
        if route["route_id"].lower() == route_id.lower():
            return route
    return None


def make_booking_id():
    global next_booking_number
    while True:
        new_id = "B" + str(next_booking_number)
        next_booking_number = next_booking_number + 1
        if new_id not in issued_ids:
            issued_ids.add(new_id)
            return new_id


def check_seat_counts():
    for route in routes:
        if route["available_seats"] < 0 or route["available_seats"] > route["total_seats"]:
            print("Internal error: seat count out of range on", route["route_id"])


def seat_status(route):
    if route["available_seats"] == 0:
        return "Fully Booked"
    elif route["available_seats"] == route["total_seats"]:
        return "Available"
    else:
        return "Partially Booked"


def show_menu():
    print()
    print("SMART BUS RESERVATION SYSTEM")
    print("================================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("================================")


def view_routes(only_available):
    print()
    print("AVAILABLE BUS ROUTES")
    print("No. | Route | Journey | Depart | Fare | Seats")
    for number, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue
        journey = route["departure_city"] + " -> " + route["destination_city"]
        if route["available_seats"] == 0:
            seats = "Fully Booked"
        else:
            seats = str(route["available_seats"]) + "/" + str(route["total_seats"])
        print(number, "|", route["route_id"], "|", journey, "|",
              route["departure_time"], "| Rs." + str(route["ticket_price"]), "|", seats)


def search_routes():
    word = input("Search by route ID or city: ").strip().lower()
    if word == "":
        print("Please type a route ID or a city name.")
        return
    found = 0
    for route in routes:
        if word == route["route_id"].lower():
            print(route["route_id"], "|", route["departure_city"], "->",
                  route["destination_city"], "| Rs.", route["ticket_price"],
                  "|", route["available_seats"], "seats available")
            found = found + 1
            break
        if word == route["departure_city"].lower() or word == route["destination_city"].lower():
            print(route["route_id"], "|", route["departure_city"], "->",
                  route["destination_city"], "| Rs.", route["ticket_price"],
                  "|", route["available_seats"], "seats available")
            found = found + 1
    else:
        if found == 0:
            print("No matching routes found.")


def book_ticket():
    print()
    print("BOOK A TICKET")

    name = input("Passenger name: ").strip()
    if name == "":
        print("Booking failed: name cannot be empty.")
        return

    age = get_number("Passenger age: ")
    if age == None or age <= 0 or age > MAX_AGE:
        print("Booking failed: age must be a whole number from 1 to", MAX_AGE)
        return

    route_id = input("Route ID (for example R101): ").strip()
    route = find_route(route_id)
    if route == None:
        print("Booking failed: route not found.")
        return

    if route["available_seats"] == 0:
        print("Booking failed: route", route["route_id"], "is Fully Booked.")
        return

    seats = get_number("Number of seats: ")
    if seats == None or seats <= 0:
        print("Booking failed: seats must be a whole number greater than zero.")
        return

    if seats > route["available_seats"]:
        print("Booking failed: only", route["available_seats"], "seat(s) available.")
        return

    booking_id = make_booking_id()
    total_fare = route["ticket_price"] * seats
    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route["route_id"],
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] = route["available_seats"] - seats
    check_seat_counts()

    print()
    print("Booking confirmed!")
    print("Booking ID:", booking_id)
    print("Passenger:", name)
    print("Route:", route["route_id"], "(" + route["departure_city"] + " -> " + route["destination_city"] + ")")
    print("Seats booked:", seats)
    print("Fare per seat: Rs.", route["ticket_price"])
    print("Total fare: Rs.", total_fare)
    print("Status: Confirmed")


def view_bookings():
    print()
    print("ALL BOOKINGS")
    if len(bookings) == 0:
        print("No bookings found.")
        return
    for number, b in enumerate(bookings, start=1):
        route = find_route(b["route_id"])
        journey = route["departure_city"] + " -> " + route["destination_city"]
        print(number, "|", b["booking_id"], "|", b["passenger_name"], "| age", b["passenger_age"],
              "|", b["route_id"], journey, "| Seats:", b["seats"],
              "| Fare: Rs.", b["total_fare"], "|", b["status"])


def cancel_booking():
    print()
    booking_id = input("Enter booking ID to cancel: ").strip().upper()

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            break
    else:
        print("Booking not found. Nothing was changed.")
        return

    if booking["status"] != "Confirmed":
        print("Booking", booking_id, "is already cancelled. Nothing was changed.")
        return

    route = find_route(booking["route_id"])
    route["available_seats"] = route["available_seats"] + booking["seats"]
    booking["status"] = "Cancelled"
    check_seat_counts()

    print("Booking", booking_id, "has been cancelled.")
    print("Seats restored:", booking["seats"])
    print("Route", route["route_id"], "available seats:", route["available_seats"])


def view_availability():
    print()
    print("SEAT AVAILABILITY")
    print("1. All routes")
    print("2. Only routes with seats remaining")
    print("3. Route schedule by departure city")
    choice = input("Choose 1-3: ").strip()

    if choice == "1":
        print()
        for route in routes:
            journey = route["departure_city"] + " -> " + route["destination_city"]
            print(route["route_id"], "|", journey, "|",
                  str(route["available_seats"]) + "/" + str(route["total_seats"]),
                  "|", seat_status(route))
    elif choice == "2":
        view_routes(True)
    elif choice == "3":
        show_schedule()
    else:
        print("Invalid choice. Enter 1, 2 or 3.")


def show_schedule():
    print()
    print("ROUTE SCHEDULE BY DEPARTURE CITY")
    for city in CITIES:
        print(city)
        found = False
        for route in routes:
            if route["departure_city"] == city:
                print("  ", route["route_id"], "->", route["destination_city"],
                      "|", route["departure_time"])
                found = True
        if found == False:
            print("   No scheduled departures.")


def generate_report():
    total_bookings = len(bookings)
    confirmed_count = 0
    cancelled_count = 0
    for b in bookings:
        if b["status"] == "Confirmed":
            confirmed_count = confirmed_count + 1
        else:
            cancelled_count = cancelled_count + 1

    seats_reserved = 0
    revenue = 0
    fully_booked = 0

    print()
    print("BOOKING REPORT")
    print("Confirmed bookings by route:")
    for route in routes:
        route_seats = 0
        route_revenue = 0
        for b in bookings:
            if b["route_id"] == route["route_id"] and b["status"] == "Confirmed":
                route_seats = route_seats + b["seats"]
                route_revenue = route_revenue + b["total_fare"]
        seats_reserved = seats_reserved + route_seats
        revenue = revenue + route_revenue
        if route["available_seats"] == 0:
            fully_booked = fully_booked + 1
        print("  ", route["route_id"], ":", route_seats, "seat(s) reserved, Rs.", route_revenue)

    print()
    print("Total bookings created:", total_bookings)
    print("Confirmed bookings:", confirmed_count)
    print("Cancelled bookings:", cancelled_count)
    print("Seats currently reserved:", seats_reserved)
    print("Confirmed revenue: Rs.", revenue)
    print("Fully booked routes:", fully_booked)


def main():
    while True:
        show_menu()
        choice_text = input("Enter your choice: ").strip()

        if not choice_text.isdigit():
            print("Please enter a number from 1 to 8.")
            continue

        choice = int(choice_text)
        if choice == 1:
            answer = input("Show only routes with seats? (y/n): ").strip().lower()
            if answer == "y":
                view_routes(True)
            else:
                view_routes(False)
        elif choice == 2:
            search_routes()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("Thank you for using Smart Bus. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")