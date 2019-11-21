#!/usr/bin/env python3
"""
@summary: the missing unittests for `py-substrate-interface`

@version: v60 (20/November/2019)
@since:   20/November/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates

@see:     two issues mentioned below
@note:    example output at bottom of this file
"""

from pprint import pprint

import substrateinterface # setup.py install

RPC_URL = "https://dev-node.substrate.dev:9933/"
# RPC_URL = "http://localhost:9933/"


def hashlib_supported_algorithms():
    """
    print all hashlib algorithms
    # py3.5.3: blake2b512 blake2s256 md4 md5 md5-sha1 ripemd160 sha1 sha224 sha256 sha384 sha512 whirlpool
    # py3.7.3: blake2b blake2b512 blake2s blake2s256 md4 md5 md5-sha1 ripemd160 sha1 sha224 sha256 sha3-224 sha3-256 sha3-384 sha3-512 sha384 sha3_224 sha3_256 sha3_384 sha3_512 sha512 sha512-224 sha512-256 shake128 shake256 shake_128 shake_256 sm3 whirlpool
    """
    import hashlib
    print (" ".join(sorted(hashlib.algorithms_available)))
     


def paramless(SI, simple_functions=["get_system_name", "get_version", "get_chain_finalised_head", "get_chain_head"]):
    """
    call all library functions which do not take a parameter 
    last one should be a block hash, e.g. "get_chain_head" because that is returned.
    """
    for func in simple_functions:
        result = getattr(SI, func)()
        print ("%25s : %s" % (func, result))
    return result # recycle the last answer


def param_block_hash(SI, block_hash):
    """
    call all library functions which take 'block_hash' as one parameter
    as the results are often complex, show only the .keys() of the answer object.
    the dict 'block_hash_functions' has tuples (fn-name, one key to explore further)
    NB: last one should be 'get_block_number' because that is returned.   
    """
    block_hash_functions=[("get_chain_block",       "block"), 
                          ("get_block_header",      "digest"), 
                          ("get_block_events",      None),
                          ("get_block_runtime_version", None),  
                          ("get_block_number",      None)]  
    
    for func, key in block_hash_functions:
        try:
            result = getattr(SI, func)(block_hash=block_hash)
            show = result.keys() if type({})==type(result) else result
            print ("%25s : %s" % (func, show), end=" ")
            if key:
                print (" --> ", key, ":", result[key].keys(), end=" ")
        except:
            pass
        print()    
    return show # recycle block_id


def param_block_id(SI, block_id):
    """
    same as above, but for library functions which take 'block_id' as one parameter.
    """
    block_id_functions=[("get_chain_block", "block"), 
                        ("get_block_hash",   None)] 
    for func, key in block_id_functions:
        try:
            result = getattr(SI, func)(block_id=block_id)
            show = result.keys() if type({})==type(result) else result
            print ("%25s : %s" % (func, show), end=" ")
            if key:
                print (" --> ", key, ":", result[key].keys(), end=" ")
        except:
            pass
        print()    

    
def metadata(SI, block_hash):
    """
    explore the answer of the 'get_block_metadata' a bit further: 
    """
    md = SI.get_block_metadata(block_hash=block_hash)
    result = md.value
    print ("%25s : %s" % ("get_block_metadata", result.keys()))
    print ("%28s" % "-->")
    print ("%29s : %s" % ("magicNumber", result["magicNumber"]))
    k=next(iter(result["metadata"].keys()))
    print ("%29s : %s" % ("key", k))
    keys=result["metadata"][k]["modules"][0].keys()
    print ("%29s : %s" % ("%s-->modules[0]" % k, keys))
    
    return result["metadata"][k]["modules"]



def get_storage_by_key(SI, block_hash, storage_key):
    """
    see issue https://github.com/polkascan/py-substrate-interface/issues/2
    """
    print ("get_storage_by_key(storage_key='%s', block_hash=%s)" % (storage_key, block_hash))
    try:
        storage = SI.get_storage_by_key(block_hash=block_hash, storage_key=storage_key)
        pprint (storage)
    except Exception as e:
        print (e) # type(e), 
    return storage


def get_storage(SI, block_hash, module, function, params=[]):
    """
    see issue https://github.com/polkascan/py-substrate-interface/issues/3
    """
    print ("Please give some examples how this works ... ")
    print ("get_storage(module='%s', function='%s', params='%s', block_hash=%s)" % (module, function, params, block_hash))
    storage = SI.get_storage(block_hash=block_hash, module=module, function=function, params=params)
    pprint (storage)


def testing_substrateinterface():
    """
    call all of the above batches of different API functions, possibly passing on some parameters to the next 
    """
    
    SI = substrateinterface.SubstrateInterface(url=RPC_URL)
    print ("Connected to:", SI.url)
    # pprint (dir(SI)); exit()
    
    print ("\n[no parameters]")
    block_hash = paramless(SI)
    
    # block_hash="0x4544711eab52cf237bfba0b85079270fce1eb3c49bf5dd4d90a130c4a78ffd35"
    # number=1
        
    print ("\n[param block_hash=%s]" % block_hash)
    number = param_block_hash(SI, block_hash)

    print ("\n[param block_hash=%s]" % block_hash)
    md = metadata(SI, block_hash)
    # pprint(md, width=120)

    print ("\n[param block_id=%s]" % number)
    number = 1 if not type(number)==int else number
    param_block_id(SI, block_id=number)

    storage_key="0x50a63a871aced22e88ee6466fe5aa5d9"
    print ("\n[params: storage_key=xxh6464('Sudo Key')='%s', block_hash=%s]" % (storage_key, block_hash))
    storage = get_storage_by_key(SI, block_hash, storage_key=storage_key)
    
    without0x = storage [2:] 
    module="Balances"; function="FreeBalance"; params=without0x
    # print ("\n[param block_hash=%s, module=%s, function=%s, params=%s]" % (block_hash, module, function, params))
    print ("\n[Unclear]")
    get_storage(SI, block_hash, module=module, function=function, params=params)
    

def get_storage_testing():
    """
    connect, get chain head, get_storage_by_key, get_storage
    """
    SI = substrateinterface.SubstrateInterface(url=RPC_URL)
    block_hash = SI.get_chain_head()
    storage_key="0x50a63a871aced22e88ee6466fe5aa5d9" # eonding of "Sudo Key"
    storage = get_storage_by_key(SI, block_hash, storage_key=storage_key)
    without0x = storage [2:] 
    get_storage(SI, block_hash, module="sudo", function="sudo", params=without0x)


if __name__ == '__main__':
    # hashlib_supported_algorithms(); exit()
    # testing_substrateinterface()
    
    get_storage_testing()




# example output:
"""
Connected to: https://dev-node.substrate.dev:9933/

[no parameters]
          get_system_name : substrate-node
              get_version : 2.0.0
 get_chain_finalised_head : 0xcad9907b1e5d13b97e02b4bde79d128a06480d4a3bc30ed83ab0c6c3b0113833
           get_chain_head : 0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194

[param block_hash=0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194]
          get_chain_block : dict_keys(['block', 'justification'])  -->  block : dict_keys(['extrinsics', 'header']) 
         get_block_header : dict_keys(['digest', 'extrinsicsRoot', 'number', 'parentHash', 'stateRoot'])  -->  digest : dict_keys(['logs']) 
         get_block_events : dict_keys(['jsonrpc', 'result', 'id']) 
get_block_runtime_version : dict_keys(['apis', 'authoringVersion', 'implName', 'implVersion', 'specName', 'specVersion']) 
         get_block_number : 381 

[param block_hash=0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194]
       get_block_metadata : dict_keys(['magicNumber', 'metadata'])
                         -->
                  magicNumber : 1635018093
                          key : MetadataV8
      MetadataV8-->modules[0] : dict_keys(['name', 'prefix', 'storage', 'calls', 'events', 'constants', 'errors'])

[param block_id=381]
          get_chain_block : dict_keys(['block', 'justification'])  -->  block : dict_keys(['extrinsics', 'header']) 
           get_block_hash : 0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194 

[params: storage_key=xxh6464('Sudo Key')='0x50a63a871aced22e88ee6466fe5aa5d9', block_hash=0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194]
get_storage_by_key(storage_key='0x50a63a871aced22e88ee6466fe5aa5d9', block_hash=0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194)
'0xd43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d'

[Unclear]
Please give some examples how this works ... 
get_storage(module='Balances', function='FreeBalance', params='d43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d', block_hash=0xbf16aa6471bef6156d0ffc23db5fb8c6063eb354ece35a6ee14904c1fba16194)

None
"""

