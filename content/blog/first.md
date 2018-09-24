---
title: "Mode Collapse"
hero_image: "hero.jpg"
date: 2018-04-24T17:44:36-07:00
description: ""
---
<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
  MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    displayMath: [['$$','$$']],
    processEscapes: true,
    processEnvironments: true,
    skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
    TeX: { equationNumbers: { autoNumber: "AMS" },
         extensions: ["AMSmath.js", "AMSsymbols.js"] }
  }
  });
  MathJax.Hub.Queue(function() {
    // Fix <code> tags after MathJax finishes running. This is a
    // hack to overcome a shortcoming of Markdown. Discussion at
    // https://github.com/mojombo/jekyll/issues/199
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
  });

  MathJax.Hub.Config({
  // Autonumbering by mathjax
  TeX: { equationNumbers: { autoNumber: "AMS" } }
  });
</script>


## **Problem**
  
Issue of mode collapse is often observed in Generative Modelling. Suppose the original distribution of the dataset is $\mathcal{P}$ and learned distribution is $\mathcal{Q}$. The mode collapse is said to be occur when sample generate from Q does not represent all the modes present in $\mathcal{P}$. For the practical purposes the definition of mode is equated to the class. So one practical example of mode collapse is a generative model train on [MNIST](http://yann.lecun.com/exdb/mnist/) dataset only samples images exclude images from certain class completely. Mode collapse is mainly observed in implicit methods of distribution learning such as GANs.

![Mode Collapse in Mixture Models](/img/gaussian_mode_collapse.png)

Above image is a representation of mode collapse issue in 1-D Gaussian Mixture Models

- ## **Why Mode Collapse Occur?**

Recent Paper such as [Arora et. al](https://arxiv.org/abs/1706.08224) have shown that finite capacity discriminators are not capable of learning complex high dimensional distributions. But any theory suggesting probable cause of mode collapse has not appeared yet. 

Efforts to resolving this effort has been largely divided into two catagories. 

### A. GAN-VAE Hybrid

The mode collapse problem has not been observed in explicit generative models such as as Variational Auto Encoders. To leverage this results many approaches have tried to mitigate mode collapse by creating a VAE-GAN hybrid. Some of the examples include: [Adversarial Autoencoders](https://arxiv.org/abs/1511.05644), [Adversarial Variational Bayes](https://arxiv.org/abs/1701.04722) , [VEEGAN](https://arxiv.org/abs/1705.07761) , [ALI](https://arxiv.org/abs/1606.00704) , [BIGAN](https://arxiv.org/abs/1605.09782) etc.

This models have either tried to add an encoder for GAN or [convert ELBO bound into implicit density learning using a classifier](https://arxiv.org/abs/1702.08235).

But some of the large scale [empirical](https://arxiv.org/abs/1802.06847),([slides](http://efrosgans.eecs.berkeley.edu/CVPR18_slides/VAE_GANS_by_Rosca.pdf)) and [theoritical](http://www.offconvex.org/2018/03/12/bigan/) studies have shown that this models have not contributed in stabilizing the training of GANs.

### B. Changing Objective Function

Another path explored by multiple research papers to solve mode collapse has been modifying the objective function of GAN. Models like [Wasserstein GAN](https://arxiv.org/abs/1701.07875) have tried using Earth Mover distance function as GAN critic. Following image does a great job of explaining multiple objective functions. 

![GAN Objective Functions](/img/gan_models.png)

[This](https://arxiv.org/pdf/1711.10337.pdf) large scale empirical study of many GAN models has argued that performance improvement reported in these models can be simply achieved by performing exhaustive parameter search in original GAN model. Many empirical results have shown that issue of mode collapse still persists in all of these models. Analysis performed by [Shibani et al.](https://arxiv.org/abs/1711.00970) have demonstrated this issue. 

- ## **Challenge in Solving Mode Collapse**

The issue of mode collapse is very closely attached with the idea of class. The existing measures of evaluating similarities in probability distribution includes divergence measure, IPM etc. None of these metrics individually provide a clear idea of distance between distributions at modes. So it becomes a crucial challenge to quantify the "*Mode Collapse*"

<!-- ### Quantifying Mode Collapse

One of the simplest way to quantify mode collapse is by using the idea of class. Suppose there exists a data space $(X,y)$ such that X is the sample and y is class label associated with it. So we define a distance measure between $\mathcal{P}$ &s $\mathcal{Q}$ such that:

`$$ \text{dist}(\mathcal{P},\mathcal{Q}) \propto D_{f}(\mathcal{P}(y|X),\mathcal{Q}(y|X)) $$`
Where $D_f$ is any divergence measure. 

But in the real data, we do not have any information regarding the class of the samples. So the natural extension of this idea is to think in terms of unsupervised learning. So we look into the clusters of the data. Let us assume that $x_1,x_2,\dots,x_n$ are sample generate by $\mathcal{P}$ and $\hat{x_1},\hat{x_2},\dots,\hat{x_n}$ are samples generated by $\mathcal{Q}$. 



The idea suggested here is very similar to [Inception score](https://arxiv.org/pdf/1801.01973.pdf). 
$$
\mathrm { IS } ( G ) = \exp \left( \mathbb { E } _ { \mathbf { x } \sim p _ { g } } D _ { K L } ( p ( y | \mathbf { x } ) \| p ( y ) ) \right)
$$
In case of inception score, $p(y|X)$ is probability of classifier assignment. Using the idea of clustering we can calculate $p(y|X)$ in following manner. 

Suppose c_1,c_2,\dots c_k are cluster centres of x_1,x_2,\dots,x_n Now,


$$
\begin{align}
p(y_k|\hat{x}i) &= \frac{exp(\hat{x}_i - c_k)}{\sum_j exp(\hat{x}_i - c_j)} \\

	&= softmax(\hat{x}_i - c_k) \quad c_k = k^{th}\text{ center mean}

\end{align}
$$






$$
\begin{align}
	p(y) &= \mathbb{E}_{x \sim p_g(x)} \left[ p(y|X) \right] \\
	p(y) &\approx \sum_{x_k}p(y|) 
\end{align}
$$ -->
