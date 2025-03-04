"""
Test healthcare system
"""

import sciris as sc
import phcsim as phc

do_plot = False


def test_products(do_plot=do_plot):
    sc.heading('Testing products')
    d = phc.load_data()
    prod = phc.Products()
    prod.init_pre(d=d)
    return prod


if __name__ == '__main__':

    do_plot = True
    sc.options(dpi=200)

    T = sc.timer()

    prod = test_products(do_plot=do_plot)

    T.toc()
