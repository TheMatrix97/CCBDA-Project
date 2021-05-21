import JobIssuer


if __name__ == "__main__":
    params = {"city": "City1", "idSimulacio": 1}
    print("Running")
    # Start simulation
    JobIssuer.start_simulation(params)
    print("Ends")
