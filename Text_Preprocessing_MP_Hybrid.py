
################################### Part 1 : Text Preprocessing ###################################
##################################### Using Multi-Processing ######################################


# OS Libraries
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import traceback


# Custom Text Preprocessor Library
from Text_Preprocessor import Text_Processor


# Data Science Libraries
# import numpy as np
import pandas as pd
from progress.bar import Bar




def Pretty_Print(text : str):
    """Pretty Printer
        =============
        Prints Text in rich format
    """
    print((' '+text+' ').center(100, '-'))
    



def save_results(results : dict[dict], df : pd.DataFrame, filePath : str):
    try: filePath = filePath[: filePath.find('.csv')] + '_processed.csv'
    except:
        filePath = "temp_dataset_processed.csv"
        print(f"Invalid file path, writing to {filePath}")

    try:

        for datum in results:
            try: df.loc[datum[0], 'Proc_Tweet'] = datum[1]
            except: print(f"Index no. {datum[0]} is errorneous")

        Pretty_Print("Final DataFrame")
        print(df)

        df.to_csv(filePath)
        Pretty_Print(f"Wrote to csv file {filePath} successfully")

    except Exception as e:
        Pretty_Print(f"Couldn't write to csv file, Error : {e}")
        print(traceback.print_exc())




################################################################
########################### Using MP ###########################
################################################################

def job_Process_MP(idx_texts, jobNo, ACK, results_dict):
    processed_data = {}

    # print(f'from job {jobNo}')
    for idx,text in idx_texts:
        processed_data[idx] = Text_Processor.CTL_Text(text)
        if ACK: print(f"{idx}. DATA : {processed_data[idx]}")
    
    results_dict[jobNo] = processed_data



def using_MP(tasks : list, noProcesses : int = 6, ACK : bool = True):
    processes : list[mp.Process] = []

    ############################################# Jobs Distribution #############################################
    jobPerProcess = len(tasks)//noProcesses
    jobs = [tasks[i*jobPerProcess : (i+1)*jobPerProcess] for i in range(noProcesses)]
    if len(tasks)%noProcesses: jobs[-1].extend(tasks[(-1)*(len(tasks)%noProcesses):])


    ############################################# Verification if all jobs got recorded #############################################
    totJobs = 0
    for job in jobs:
        totJobs += len(job)

    Pretty_Print(f'Recorded Jobs : {totJobs}, Expected Jobs : {len(tasks)}, Expected Processes : {noProcesses}, Job Per Process : {jobPerProcess}')

    MP_Manager = mp.Manager()
    results_dict = MP_Manager.dict()

    for jobNo,job in enumerate(jobs, 1):
        prcs = mp.Process(target=job_Process_MP, args=(job, jobNo, ACK, results_dict))
        prcs.start()
        processes.append(prcs)

    for process in processes:
        process.join()

    Pretty_Print(f'No of Processes : {len(processes)}')

    results = []
    i = 1
    for datum in results_dict.values():
        for idx, chunk in datum.items():
            print(f"{i}. DATA : ", chunk, type(chunk), idx)
            results.append((idx, chunk,))
            i += 1
    
    return results




#################################################################
########################### Using PPE ###########################
#################################################################

def job_Process_PPE(idx_texts):
    idx, text = idx_texts
    pro = Text_Processor.CTL_Text(text)
    return (idx, pro,)


def using_PPE(tasks : list, noProcesses : int = 6, ACK : bool = True):
    print('\n\n')
    bar = Bar('Processing...', max=len(tasks), fill='#')#, suffix='%(percent).1f%% - %(eta)ds')

    results = []
    with ProcessPoolExecutor(max_workers = noProcesses) as executor:
        future_res = executor.map(job_Process_PPE, tasks)
        for result in future_res:
            results.append(result)
            if ACK: print(f"ACK : {result[0]}. {result[1]}")
            else: bar.next()
    print()

    return results






def Multi_Processor():
    ############################################# Creating Jobs #############################################
    try:
        Pretty_Print("Creating Jobs...")
        filePath = input("\n\t Enter Path to dataset : ")
        try:
            df = pd.read_csv(filePath)
        except:
            raise(f"Error while reading dataset from {filePath}")

        df['Proc_Tweet'] = ""
        df = df.loc[:100, :]

        texts = []
        for idx in df.index:
            texts.append((idx, df.loc[idx, 'content'],))


        ############################################# Essential Variables Declaration #############################################
        noProcesses = 6
        requestedProcesses = input(f"\n\t How many concurrent parallel processes you want to spawn (1 - 50)? (default {noProcesses}) : ")
        try:
            requestedProcesses = int(float(requestedProcesses))
            if requestedProcesses in range(1, 51): noProcesses = requestedProcesses
        except: print(f"Invalid Process Count, chosen count = {noProcesses}")

        input("\n\t Do you want to create Checkpoints to stroe job results ? Enter Job count for Checkpoint (default 10%): ")

        ACK_decision = input("\n\t Do you want Continuous ACKnowledgement of job completions (y/Y/yes/Yes) for Yes (default Yes) : ")
        ACK = ACK_decision in ("", "y", "Y", "yes", "Yes",)


        ############################################# Initiating Multiple Concurrent Processes #############################################
        Pretty_Print('Initiating Multi-Processing...')
        MP_SrtTime = time.perf_counter()

        decide = input("\n\t 1. Process Pool Executor (faster)(default) \n\t 2. Standard Multi-Processing\n\t Choose Multi-Processing Method : ")
        try:
            decide = abs(int(float(decide)))%3
        except: decide = 1
        if decide == 2: results = using_MP(texts, noProcesses, ACK)
        else:           results = using_PPE(texts, noProcesses, ACK)

        MP_EndTime = time.perf_counter()


        ############################################# Writing Processed data to Files #############################################
        # save_results(results, df, filePath + "_processed")
        
        Pretty_Print(f'Multi-Processing Time Lapse : {round(MP_EndTime-MP_SrtTime, 2)}')
    
    except:
        df.to_csv("temp_dataset.csv")
        Pretty_Print(f"Some error Occurred, Progress till now (if any) saved to ./temp_dataset.csv")




if __name__ == '__main__':
    programSrtTime = time.perf_counter()
    print('\n\n\n')
    try: Multi_Processor()
    except: Pretty_Print("Error....")
    Pretty_Print(f'Total Time Lapse : {round(time.perf_counter()-programSrtTime, 2)}')