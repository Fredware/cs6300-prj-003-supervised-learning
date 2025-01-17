import numpy as np

import nn


class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        score = self.run(x)
        if nn.as_scalar(score) >= 0:
            pred_val = 1
        else:
            pred_val = -1
        return pred_val

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        agg_mse = 1
        while agg_mse != 0:
            agg_mse = 0
            for x, y in dataset.iterate_once(batch_size):
                y_pred = self.get_prediction(x)
                agg_mse += (int(nn.as_scalar(y)) - y_pred) ** 2
                if y_pred != int(nn.as_scalar(y)):
                    self.w.update(x, nn.as_scalar(y))


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        h1 = 5
        h2 = 20
        h3 = 5
        self.w1 = nn.Parameter(1, h1)
        self.b1 = nn.Parameter(1, h1)

        self.w2 = nn.Parameter(h1, h2)
        self.b2 = nn.Parameter(1, h2)

        self.w3 = nn.Parameter(h2, h3)
        self.b3 = nn.Parameter(1, h3)

        self.w4 = nn.Parameter(h3, 1)
        self.b4 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        z1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        z2 = nn.ReLU(nn.AddBias(nn.Linear(z1, self.w2), self.b2))
        z3 = nn.ReLU(nn.AddBias(nn.Linear(z2, self.w3), self.b3))
        y_pred = nn.AddBias(nn.Linear(z3, self.w4), self.b4)
        return y_pred

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        y_hat = self.run(x)
        return nn.SquareLoss(y_hat, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 5
        alpha = -1e-3

        min_loss = np.inf
        while min_loss > 0.00005:
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                # if nn.as_scalar(loss)<=prev_loss+0.25:
                grad_w1, grad_b1, grad_w2, grad_b2, grad_w3, grad_b3, grad_w4, grad_b4 = nn.gradients(loss,
                                                                                                      [
                                                                                                          self.w1,
                                                                                                          self.b1,
                                                                                                          self.w2,
                                                                                                          self.b2,
                                                                                                          self.w3,
                                                                                                          self.b3,
                                                                                                          self.w4,
                                                                                                          self.b4
                                                                                                      ])
                self.w1.update(grad_w1, alpha)
                self.b1.update(grad_b1, alpha)
                self.w2.update(grad_w2, alpha)
                self.b2.update(grad_b2, alpha)
                self.w3.update(grad_w3, alpha)
                self.b3.update(grad_b3, alpha)
                self.w4.update(grad_w4, alpha)
                self.b4.update(grad_b4, alpha)
                # print(nn.as_scalar(loss))
                min_loss = min(min_loss, nn.as_scalar(loss))


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        h1 = 200
        h2 = 100
        h3 = 30
        h4 = 15

        self.w1 = nn.Parameter(784, h1)
        self.b1 = nn.Parameter(1, h1)

        self.w2 = nn.Parameter(h1, h2)
        self.b2 = nn.Parameter(1, h2)

        self.w3 = nn.Parameter(h2, h3)
        self.b3 = nn.Parameter(1, h3)

        self.w4 = nn.Parameter(h3, h4)
        self.b4 = nn.Parameter(1, h4)

        self.w5 = nn.Parameter(h4, 10)
        self.b5 = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        z1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        z2 = nn.ReLU(nn.AddBias(nn.Linear(z1, self.w2), self.b2))
        z3 = nn.ReLU(nn.AddBias(nn.Linear(z2, self.w3), self.b3))
        z4 = nn.ReLU(nn.AddBias(nn.Linear(z3, self.w4), self.b4))
        y_pred = nn.AddBias(nn.Linear(z4, self.w5), self.b5)
        return y_pred

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        y_pred = self.run(x)
        return nn.SoftmaxLoss(y_pred, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 20
        while True:
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                grad_w1, grad_b1, grad_w2, grad_b2, grad_w3, grad_b3, grad_w4, grad_b4 = nn.gradients(loss,
                                                                                                      [
                                                                                                          self.w1,
                                                                                                          self.b1,
                                                                                                          self.w2,
                                                                                                          self.b2,
                                                                                                          self.w3,
                                                                                                          self.b3,
                                                                                                          self.w4,
                                                                                                          self.b4
                                                                                                      ])

                val_acc = dataset.get_validation_accuracy()
                # print(val_acc)
                if val_acc > 0.973:
                    return
                elif val_acc > 0.970:
                    alpha = -5e-3
                elif val_acc > 0.960:
                    alpha = -5e-2
                elif val_acc > 0.750:
                    alpha = -1e-1
                elif val_acc > 0.450:
                    alpha = -5e-1
                else:
                    alpha = -5.5e-1

                self.w1.update(grad_w1, alpha)
                self.b1.update(grad_b1, alpha)
                self.w2.update(grad_w2, alpha)
                self.b2.update(grad_b2, alpha)
                self.w3.update(grad_w3, alpha)
                self.b3.update(grad_b3, alpha)
                self.w4.update(grad_w4, alpha)
                self.b4.update(grad_b4, alpha)


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        d = 100
        self.W = nn.Parameter(self.num_chars, d)
        self.W_hidden = nn.Parameter(d, d)
        self.W_out = nn.Parameter(d, len(self.languages))
        self.b_out = nn.Parameter(1, len(self.languages))

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        for i, x in enumerate(xs):
            if i == 0:
                z = nn.ReLU(nn.Linear(x, self.W))
            else:
                z = nn.ReLU(nn.Add(nn.Linear(x, self.W), nn.Linear(z, self.W_hidden)))
        # print(z)
        y = nn.AddBias(nn.Linear(z, self.W_out), self.b_out)
        return y

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        alpha = -1e-2
        batch_size = 10
        while True:
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                val_acc = dataset.get_validation_accuracy()
                if val_acc > 0.90:
                    return
                grad_w, grad_w_hidden, grad_w_out, grad_b_out = nn.gradients(loss,
                                                                             [
                                                                                 self.W,
                                                                                 self.W_hidden,
                                                                                 self.W_out,
                                                                                 self.b_out
                                                                             ])
                self.W.update(grad_w, alpha)
                self.W_hidden.update(grad_w_hidden, alpha)
                self.W_out.update(grad_w_out, alpha)
                self.b_out.update(grad_b_out, alpha)
