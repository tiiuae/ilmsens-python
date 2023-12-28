import os
import glob
import scipy.io
import numpy as np
import ilmsens_hal.utils


def equals(a: np.ndarray, b: np.ndarray) -> bool:
    if a.shape != b.shape:
        return False
    for ai, bi in zip(a.flat, b.flat):
        if ai != bi:
            return False
    return True

def avgdiff(a: np.ndarray, b: np.ndarray) -> float:
    return (a - b).mean()


dir_path = os.path.dirname(os.path.abspath(__file__))
test_cases = glob.glob(os.path.join(dir_path, "ideal_outputs", "*.mat"))

passed = True
for i, test_case_path in enumerate(test_cases):
    test_case = scipy.io.loadmat(test_case_path)

    print("\nTest Case #{}: (Order: {}; Oversampling: {})"
          .format(i+1, test_case["mDR_MLBS_Order"].item(), test_case["mDR_OV"].item()))

    try:
        output = ilmsens_hal.utils.drPropDependencies(
            mDR_F0_Clk=test_case["mDR_F0_Clk"].item(),
            mDR_OV=test_case["mDR_OV"].item(),
            mDR_MLBS_Order=test_case["mDR_MLBS_Order"].item(),
        )
    except:
        passed = False

    print("Outputs:")

    ## Test @mDR_Ref_MLBS
    test_case["mDR_Ref_MLBS"] = test_case["mDR_Ref_MLBS"].astype(float)
    if equals(output["mDR_Ref_MLBS"], test_case["mDR_Ref_MLBS"][:, 0]):
        print("   @ mDR_Ref_MLBS > Ok")
    else:
        print("   @ mDR_Ref_MLBS > Error")
        passed = False

    ## Test @mDR_Ref_Spec
    error_thres = 1e-16
    mean_difference = avgdiff(output["mDR_Ref_Spec"].real, test_case["mDR_Ref_Spec"][:, 0].real)
    if mean_difference.real < error_thres:
        print("   @ mDR_Ref_Spec.real > Ok")
    else:
        print("   @ mDR_Ref_Spec.real > Error")
        print("                       > Mean Difference: {:.32f} ({})".format(mean_difference, mean_difference))
        print("                       > Target Values Range: [{:.32f} .. {:.32f}]"
              .format(test_case["mDR_Ref_Spec"][:, 0].real.min(), test_case["mDR_Ref_Spec"][:, 0].real.max()))
        passed = False

    mean_difference = avgdiff(output["mDR_Ref_Spec"].imag, test_case["mDR_Ref_Spec"][:, 0].imag)
    if mean_difference.imag < error_thres:
        print("   @ mDR_Ref_Spec.imag > Ok")
    else:
        print("   @ mDR_Ref_Spec.imag > Error")
        print("                       > Mean Difference: {:.32f} ({})".format(mean_difference, mean_difference))
        print("                       > Target Values Range: [{:.32f} .. {:.32f}]"
              .format(test_case["mDR_Ref_Spec"][:, 0].imag.min(), test_case["mDR_Ref_Spec"][:, 0].imag.max()))
        passed = False

    ## Test @mDR_Ref_Times
    if equals(output["mDR_Ref_Times"], test_case["mDR_Ref_Times"][:, 0]):
        print("   @ mDR_Ref_Times > Ok")
    else:
        print("   @ mDR_Ref_Times > Error")
        passed = False

    ## Test @mDR_Ref_Frqs
    if equals(output["mDR_Ref_Frqs"], test_case["mDR_Ref_Frqs"][:, 0]):
        print("   @ mDR_Ref_Frqs > Ok")
    else:
        print("   @ mDR_Ref_Frqs > Error")
        passed = False


if passed:
    print("\nPassed!")
else:
    print("\nFailed!")
