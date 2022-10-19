import numpy as np
import geoglows as geo
import pandas as pd

reach_id = 9031111

path_to_fdc_zarr = "/path/to/FDCs/fdc_"+str(reach_id)+".zarr"


def retrieve_data(a):
    q_hist = geo.streamflow.historic_simulation(a)
    return q_hist


def save_as_zarr():
    hist = retrieve_data(reach_id)
    # sort in descending order
    sort = hist.sort_values(by='streamflow_m^3/s', ascending=False)
    exceedence = np.arange(1., len(sort)+1) / len(sort)

    # save each computed flow duration curve in a zarr file
    data_dict = {
        'streamflow_from_high_to_low': sort['streamflow_m^3/s'],
        'exceedence_probability': list(exceedence)
    }
    ts_dataframe = pd.DataFrame(data_dict)
    ts_dataset = ts_dataframe.to_xarray()
    ts_dataset.to_zarr(path_to_fdc_zarr)
    ts_dataset.close()


save_as_zarr()
