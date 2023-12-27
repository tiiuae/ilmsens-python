import os
import struct
import numpy as np
from ctypes import sizeof
from ilmsens_hal.ilmsens_hal_types import ilmsens_hal_MemoryType



def parse_data(buffer) -> tuple:
    num_samples = 511
    s = sizeof(ilmsens_hal_MemoryType)
    rx1_samples = buffer[:num_samples*s]
    seq_counter = buffer[num_samples*s:(num_samples*s)+4]
    rx2_samples = buffer[(num_samples*s)+4:2*(num_samples*s)+4]
    reserved = buffer[2*(num_samples*s)+4:]

    rx1_samples = struct.unpack("<%di" % (len(rx1_samples)//4), rx1_samples)
    rx2_samples = struct.unpack("<%di" % (len(rx2_samples)//4), rx2_samples)
    seq_counter = struct.unpack("<%di" % (len(seq_counter)//4), seq_counter)

    return {
        "seq_counter": seq_counter,
        "rx1_samples": rx1_samples,
        "rx2_samples": rx2_samples,
        "reserved": reserved
    }



def drPropDependencies(mDR_F0_Clk: float = 13.312, mDR_OV: int = 1, mDR_MLBS_Order: int = 9) -> dict:
    mDR_Ref_MLBS = None
    mDR_Ref_Spec = None
    mDR_Ref_Times = None
    mDR_Ref_Frqs = None

    if mDR_OV > 1:
        raise NotImplementedError
    if mDR_MLBS_Order not in [9, 15]:
        raise NotImplementedError

    tNumSamp = (2**(mDR_MLBS_Order)-1)*mDR_OV
    tTimeStep = 1/(mDR_F0_Clk*mDR_OV)
    mDR_Ref_Times = np.arange(tNumSamp).T * tTimeStep

    tFrqStep = 1/(tTimeStep*tNumSamp)
    mDR_Ref_Frqs = np.fft.ifftshift(np.arange(np.ceil(-tNumSamp/2), np.ceil(tNumSamp/2)) * tFrqStep)

    tNumSamp = 2**(mDR_MLBS_Order)-1
    tMLBSName = f"mlbs{mDR_MLBS_Order}.txt"
    dirName = os.path.dirname(os.path.abspath(__file__))
    tMLBSOrg = np.loadtxt(os.path.join(dirName, tMLBSName))
    tMLBSOrg = tMLBSOrg.reshape(-1)
    tMLBSOrg = tMLBSOrg[:tNumSamp]

    tMLBSOrg = np.expand_dims(tMLBSOrg, axis=1)
    tBB_MLBS = np.repeat(tMLBSOrg, mDR_OV, axis=1)

    tF0_MLBS = tBB_MLBS.T * np.sin(2*np.pi*mDR_F0_Clk * mDR_Ref_Times)
    tF0_MLBS = tF0_MLBS.T

    if mDR_OV > 1:
        mDR_Ref_MLBS = tBB_MLBS + tF0_MLBS # ideal baseband + up-mixed MLBS as reference signal
    else:
        mDR_Ref_MLBS = tBB_MLBS # ideal baseband MLBS as reference signal

    mDR_Ref_Spec = np.conj(np.exp(1j*np.angle(np.fft.fft(mDR_Ref_MLBS, axis=0))))
    mDR_Ref_Spec[0] = 0

    return {
        "mDR_Ref_MLBS": mDR_Ref_MLBS,
        "mDR_Ref_Spec": mDR_Ref_Spec,
        "mDR_Ref_Times": mDR_Ref_Times,
        "mDR_Ref_Frqs": mDR_Ref_Frqs,
    }
