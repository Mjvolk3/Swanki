Bayes' theorem can be found in terms of the quantities in the numerator, using

\[
p(\mathbf{x})=\sum_{k} p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)
\]

Equivalently, we can model the joint distribution \(p\left(\mathbf{x}, \mathcal{C}_{k}\right)\) directly and then normalize to obtain the posterior probabilities. Having found the posterior probabilities, we use decision theory to determine the class membership for each new input \(\mathbf{x}\). Approaches that explicitly or implicitly model the distribution of inputs as well as outputs are known as generative models, because by sampling from them, it is possible to generate synthetic data points in the input space.

(b) First, solve the inference problem of determining the posterior class probabilities \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\), and then subsequently use decision theory to assign each new \(\mathbf{x}\) to one of the classes. Approaches that model the posterior probabilities directly are called discriminative models.

(c) Find a function \(f(\mathbf{x})\), called a discriminant function, that maps each input \(\mathbf{x}\) directly onto a class label. For instance, for two-class problems, \(f(\cdot)\) might be binary valued and such that \(f=0\) represents class \(\mathcal{C}_{1}\) and \(f=1\) represents class \(\mathcal{C}_{2}\). In this case, probabilities play no role.

Let us consider the relative merits of these three alternatives. Approach (a) is the most demanding because it involves finding the joint distribution over both \(\mathrm{x}\) and \(\mathcal{C}_{k}\). For many applications, \(\mathrm{x}\) will have high dimensionality, and consequently, we may need a large training set to be able to determine the class-conditional densities to reasonable accuracy. Note that the class priors \(p\left(\mathcal{C}_{k}\right)\) can often be estimated simply from the fractions of the training set data points in each of the classes. One advantage of approach (a), however, is that it also allows the marginal density of data \(p(\mathbf{x})\) to be determined from (5.25). This can be useful for detecting new data points that have low probability under the model and for which the predictions may be of low accuracy, which is known as outlier detection or novelty detection (Bishop, 1994; Tarassenko, 1995).

However, if we wish only to make classification decisions, then it can be wasteful of computational resources and excessively demanding of data to find the joint distribution \(p\left(\mathbf{x}, \mathcal{C}_{k}\right)\) when in fact we really need only the posterior probabilities \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\), which can be obtained directly through approach (b). Indeed, the classconditional densities may contain a significant amount of structure that has little effect on the posterior probabilities, as illustrated in Figure 5.8. There has been much interest in exploring the relative merits of generative and discriminative approaches to machine learning and in finding ways to combine them (Jebara, 2004; Lasserre, Bishop, and Minka, 2006).

An even simpler approach is (c) in which we use the training data to find a discriminant function \(f(\mathbf{x})\) that maps each \(\mathbf{x}\) directly onto a class label, thereby combining the inference and decision stages into a single learning problem. In the example of Figure 5.8, this would correspond to finding the value of \(x\) shown by