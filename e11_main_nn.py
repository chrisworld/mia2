# Torch Module:----------------------------------------------------------------
import torch 
import torch.optim as optim
from torch.utils.data import SubsetRandomSampler

# Import User defined MLP and customData class:--------------------------------
import MLP
import customData

# Import User defined label_to_index function:---------------------------------
from mia2 import label_to_index

# Import numpy, matplotlib and scipy helper functions:-------------------------
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
if __name__ == "__main__":
    
    # Part 1 - Loading:--------------------------------------------------------
    plot_path = 'ignore/ass10_data/plots/'
    file_path = './ignore/ass11_data/BspDrums.mat'
    
    data_set = customData.CustomDataSetFromMat( file_path, 'drumFeatures' )
    
    # Convert drum_labels to integers
    unique_flags = np.unique( data_set.drum_labels )
    
    data_set.drum_labels = label_to_index( data_set.drum_labels, unique_flags )
    data_set.drum_labels = torch.tensor( data_set.drum_labels, 
        dtype=torch.float64, requires_grad=False )
      
    # Part 2 - Set default torch model data type:------------------------------
    torch.set_default_dtype( torch.float64 )

    # Part 3 - Instantiate Neural Net:-----------------------------------------
    in_dim, hid_dim, out_dim = ( 45, 2, 3 )
    net = MLP.MLP_Net( in_dim, hid_dim, out_dim )

    # Print all net parameters onto the screen
    # print( "Neural Network parameters {}".format( list( net.parameters( ) ) ) )

    # Define a loss function and choose an optimizer
    criterion = torch.nn.MSELoss( reduction='mean' )
    optimizer = optim.SGD( net.parameters( ), lr=0.001, momentum=0.9 )

    # Part 4 - Generate Training and Test set:---------------------------------
    # The following code is based on https://bit.ly/3dAxv5S    
    train, valid, test = data_set.generate_sets( data_set.__len__( ), 
        0.6, 0.2 ) 

    # For more information:
    # - https://bit.ly/2NzOASO
    # 
    # For SubsetRandomSampler(  ):
    # - https://bit.ly/3eL1cm3 
    train_sampler = SubsetRandomSampler( train )
    valid_sampler = SubsetRandomSampler( valid )
    test_sampler = SubsetRandomSampler( test )

    train_loader = torch.utils.data.DataLoader( data_set, batch_size=4,
        num_workers=0, sampler=train_sampler)

    valid_loader = torch.utils.data.DataLoader( data_set, batch_size=4,
        num_workers=0, sampler=valid_sampler)

    testloader = torch.utils.data.DataLoader( data_set, batch_size=4,
        num_workers=0, sampler=test_sampler )

    # Train the network
    num_epochs = 100
    for epoch in range( num_epochs ):
        running_loss = 0.0
        for i , data in enumerate( train_loader, 0 ):
            # get the inputs; data is a list of [ inputs, labels ]
            inputs, labels = data

            # Zero the parameter gradients, otherwise we would 
            # accumulate the gradients for each loop iteration! 
            optimizer.zero_grad(  )

            # Forward + Backward + optimize
            outputs = net( inputs )
            loss = criterion( outputs, labels.view( -1, 1 ) )
            loss.backward(  )
            optimizer.step(  )

            # print statistics
            running_loss += loss.item(  )
            # if i % 10 == 9:
            #     print( "[%d, %5d] loss %.3f" % ( epoch + 1 , i + 1, 
            #         running_loss / 10 ) )
            #     running_loss = 0.0
                  
    print( 'Finished Training' )