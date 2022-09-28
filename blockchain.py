from blockchain import *
import copy


if __name__ == "__main__":
    state = {u'Alice':50, u'Bob':50}  # Define the initial state
    genesisBlockTxns = [state]
    genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
    genesisHash = hashMe( genesisBlockContents )
    genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
    genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

    chain = [genesisBlock]

    blockSizeLimit = 5  # Arbitrary number of transactions per block-
                   #  this is chosen by the block miner, and can vary between blocks!

    while len(txnBuffer) > 0:
        bufferStartSize = len(txnBuffer)

        ## Gather a set of valid transactions for inclusion
        txnList = []
        while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
            newTxn = txnBuffer.pop()
            validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid

            if validTxn:           # If we got a valid state, not 'False'
                txnList.append(newTxn)
                state = updateState(newTxn,state)
            else:
                print("ignored transaction")
                sys.stdout.flush()
                continue  # This was an invalid transaction; ignore it and move on

    ## Make a block
    myBlock = makeBlock(txnList,chain)
    chain.append(myBlock)

    print(chain[0])
    print(chain[1])
    print(state)

    checkChain(chain)

    chainAsText = json.dumps(chain,sort_keys=True)
    checkChain(chainAsText)

    nodeBchain = copy.copy(chain)
    nodeBtxns  = [makeTransaction() for i in range(5)]
    newBlock   = makeBlock(nodeBtxns,nodeBchain)
    print("Blockchain on Node A is currently %s blocks long"%len(chain))

    try:
        print("New Block Received; checking validity...")
        state = checkBlockValidity(newBlock,chain[-1],state) # Update the state- this will throw an error if the block is invalid!
        chain.append(newBlock)
    except:
        print("Invalid block; ignoring and waiting for the next block...")

    print("Blockchain on Node A is now %s blocks long"%len(chain))