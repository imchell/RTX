def get_data_from_db():
    from rtxlib.rtx_run import setup_database, db

    index = "rtx752"
    knob = "route_random_sigma"
    knob_values = [0.0, 0.2, 0.4, 0.6]
    y_key = 'overhead'

    setup_database(index)
    results = db().get_all_data_points()
    data = {}

    print "~~~~~~~~~"
    print index
    print "~~~~~~~~~"
    for i in knob_values:
        res = [r for r in results if r[1].get(knob)==i]
        data[i] = [r[0][y_key] for r in res]
        print str(i)+"'s: " + str(len(data[i]))

    return data


def generate_complaints(all_data, complaint_threshold):
    all_complaints = {}

    for data in all_data:
        complaints = []
        for d in all_data[data]:
            if d > complaint_threshold:
                complaints.append(1)
            else:
                complaints.append(0)
        all_complaints[data] = complaints

    return all_complaints


def save_dict_to_file(all_complaints, file_name):
    import pickle
    pickle_out = open(file_name,"wb")
    pickle.dump(all_complaints, pickle_out)
    pickle_out.close()
    print "data saved to file " + file_name


def retrieve_dict_from_file(file_name):
    import pickle
    pickle_in = open(file_name,"rb")
    all_complaints = pickle.load(pickle_in)
    return all_complaints


if __name__ == '__main__':

    route_random_sigma_data = get_data_from_db()
    save_dict_to_file(route_random_sigma_data, "route_random_sigma_data.pickle")

    complaint_threshold = 2.5

    route_random_sigma_data = retrieve_dict_from_file("route_random_sigma_data.pickle")
    # route_random_sigma_data is a dict from keys [0, 0.2, 0.4, 0.6] to list of floats representing overheads

    print "retrieved route_random_sigma_data"
    for route_random_sigma_key in sorted(route_random_sigma_data):
        print str(route_random_sigma_key) + ": " + str(len(route_random_sigma_data[route_random_sigma_key]))

    generated_complaints = generate_complaints(route_random_sigma_data, complaint_threshold)

    print "generated complaints"
    for complaint_key in sorted(generated_complaints):
        print str(complaint_key) + ": " + str(len([d for d in generated_complaints[complaint_key] if d==1]))

    save_dict_to_file(generated_complaints, "complaints_data.pickle")

    complaints_data = retrieve_dict_from_file("complaints_data.pickle")
    # complaints_data is a dict from keys [0, 0.2, 0.4, 0.6] to list of integers in [0,1] representing complaints

    print "retrieved complaints_data"
    for complaint_key in sorted(complaints_data):
        print str(complaint_key) + ": " + str(len([d for d in complaints_data[complaint_key] if d==1]))