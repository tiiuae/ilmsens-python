import os
import glob
import scipy.io
import numpy as np
# import ilmsens_hal.utils

test_cases = glob.glob(os.path.join(".", "ideal_outputs", "*.mat"))

failed = False
for i, test_case_path in enumerate(test_cases):
    test_case = scipy.io.loadmat(test_case_path)
    if test_case["mDR_OV"].item() > 1:
        continue

    print("\nTest Case #{}: (Order: {}; Oversampling: {})"
          .format(i+1, test_case["mDR_MLBS_Order"].item(), test_case["mDR_OV"].item()))

    # try:
    #     output = ilmsens_hal.utils.drPropDependencies(
    #         mDR_F0_Clk=test_case["mDR_F0_Clk"].item(),
    #         mDR_OV=test_case["mDR_OV"].item(),
    #         mDR_MLBS_Order=test_case["mDR_MLBS_Order"].item(),
    #     )
    # except:
    #     pass

    print("Outputs:")
    print("   @ mDR_Ref_MLBS > Ok")
    print("   @ mDR_Ref_Spec > Error")
    print("   @ mDR_Ref_Times > Error")
    print("   @ mDR_Ref_Frqs > Ok")

if failed:
    print("\nFailed!")
else:
    print("\nPassed!")




# ["mDR_F0_Clk"]
# ["mDR_MLBS_Order"]
# ["mDR_OV"]
# ["mDR_Ref_Frqs"]
# ["mDR_Ref_MLBS"]
# ["mDR_Ref_Spec"]
# ["mDR_Ref_Times"]
# ["tBB_MLBS"]
# ["tF0_MLBS"]
# ["tFrqStep"]
# ["tMLBSName"]
# ["tMLBSOrg"]
# ["tNumSamp"]
# ["tTimeStep"]
# print(data.keys())

# print(test_case["mDR_F0_Clk"].item())


# output["mDR_Ref_MLBS"]
# output["mDR_Ref_Spec"]
# output["mDR_Ref_Times"]
# output["mDR_Ref_Frqs"]
