    
## How does transfer learning work according to the schematic in Figure 6.13?

![](https://cdn.mathpix.com/cropped/2024_05_26_802d1a9c0b0fab763da6g-1.jpg?height=362&width=1453&top_left_y=210&top_left_x=172)

%

Transfer learning involves training a network first on a task with abundant data, such as object classification of natural images. The early layers of this pre-trained network are then copied to a new network intended for a different but related task with a smaller dataset. The final few layers of this new network are retrained to ensure that it generalizes well on the new task without overfitting due to the limited data.

- #machine-learning, #transfer-learning.intro, #deep-learning
    
---

## What modification is made to the network for a new task in transfer learning as depicted in Figure 6.13?

![](https://cdn.mathpix.com/cropped/2024_05_26_802d1a9c0b0fab763da6g-1.jpg?height=362&width=1453&top_left_y=210&top_left_x=172)

%

In transfer learning, the early layers of a pre-trained network (shown in red) are preserved, and only the final few layers (shown in blue) are retrained on a new task. This approach leverages the features learned from the original abundant dataset while adapting the model to the new, more specific task.

- #machine-learning, #transfer-learning.network-architecture, #image-classification