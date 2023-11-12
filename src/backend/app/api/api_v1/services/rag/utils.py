import functools
import re
import sys
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import g4f
from loguru import logger

from functools import lru_cache, update_wrapper


def ttl_cache(maxsize: int = 128, typed: bool = False, ttl: int = -1):
    if ttl <= 0:
        ttl = 65536
    hash_gen = _ttl_hash_gen(ttl)
    def wrapper(func):
        @lru_cache(maxsize, typed)
        def ttl_func(ttl_hash, *args, **kwargs):
            return func(*args, **kwargs)
        def wrapped(*args, **kwargs):
            th = next(hash_gen)
            return ttl_func(th, *args, **kwargs)
        return update_wrapper(wrapped, func)
    return wrapper

def _ttl_hash_gen(seconds: int):
    start_time = time.time()
    while True:
        h = hash((seconds, time.time() - start_time))
        yield h

@ttl_cache(ttl=60*3)
def get_fastest_provider(providers: list[g4f.Provider] = None, excluded_providers: list[str] = None,
                         timeout: int = 3):
    results = []
    fastest_provider = ["NO WORKING PROVIDERS", 99999]
    if providers is None:
        providers = g4f.Provider.__all__
    excluded = set(["BaseProvider", "AsyncProvider", "AsyncGeneratorProvider","RetryProvider"])
    if excluded_providers is not None:
        excluded.update(set(exluded_providers))
    providers = [p for p in providers if p not in excluded ]
    executor = ThreadPoolExecutor(max_workers=len(providers)) 
    futures = [
        executor.submit(process_provider, pname, results, fastest_provider)
        for pname in providers
    ]
    time.sleep(timeout)
    executor.shutdown(wait=False)
    try:
        for future in futures:
            future.cancel()
    except TimeoutError:
        logger.info(f"Error: Timeout")
        # for pname, future in futures:
        #     try:
        #         future.result(timeout=timeout)
        #     except TimeoutError:
        #         logger.info(f"[BROKEN]:  {pname}, Error: Timeout")

    logger.info("====== WORKING PROVIDERS ======")
    for pname, time_taken in results:
        logger.info(f"{pname:<20} {time_taken:.2f}s")

    logger.info("====== FASTEST PROVIDER ======")
    logger.info(f"{fastest_provider[0]:<20} {fastest_provider[1]:.2f}s")

    logger.debug(f"====== {len(results)}/{len(providers)} WORKING ======")
    fastest_name=  fastest_provider[0]
    fastest_provder_cls = g4f.Provider.ProviderUtils.convert[fastest_name]
    return fastest_provder_cls

def process_provider(pname, results, fastest_provider, model_name="gpt-3.5-turbo"):
    try:
        logger.info(f"[TRYING]:  {pname}")
        start_time = time.time()
        response = g4f.ChatCompletion.create(
            model=model_name,
            provider=getattr(getattr(getattr(sys.modules[__name__], "g4f"), "Provider"), pname),
            messages=[{"role": "user", "content": "Hello"}],
        )
        if response.strip() == "":
            raise Exception("Empty result")
        if "support@chatbase.co" in response:
            raise Exception("ChatBase.co")
        end_time = time.time()
        time_taken = end_time - start_time
        results.append((pname, end_time - start_time))
        # logger.debug(f"[WORKING]: {pname}, Time taken: {time_taken:.2f} seconds")
        if time_taken < fastest_provider[1]:
            fastest_provider[0] = pname
            fastest_provider[1] = time_taken
    except Exception as e:
        pass
        # logger.debug(f"[BROKEN]:  {pname}, Error: {str(e)}")



if __name__ == "__main__":
    from langchain.llms.base import LLM

    from langchain_g4f import G4FLLM
    provider=get_fastest_provider()
    # provider = [ prov for prov in g4f.providers if prov.__name__ == provider][0]
    # provider = g4f.Provider.ProviderUtils.convert[provider]
    # provider=None 
    # provider =g4f.models.gpt_35_turbo.best_provider
    llm: LLM = G4FLLM(
        model=g4f.models.gpt_35_turbo,
        provider=provider ,
    )

    res = llm("What is your knowledge cutoff date?")
    logger.info(res)  # Hello! How can I assist you today?
