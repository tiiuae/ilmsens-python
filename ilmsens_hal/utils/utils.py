import os
import struct
import numpy as np
from ctypes import sizeof
from ilmsens_hal.types import ilmsens_hal_MemoryType



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



def read_dependencies(mDR_MLBS_Order: int = 9, mDR_F0_Clk: float = 13.312, mDR_OV: int = 1) -> dict:
    mDR_Ref_Spec = None
    mDR_Ref_MLBS = None
    mDR_Ref_Times = None
    mDR_Ref_Frqs = None

    if mDR_MLBS_Order not in [9, 12, 15]:
        raise NotImplementedError("Only implemented for 9-th, 12-th and 15-th order m-sequence.")

    # prepare delay time and frequency axis
    tNumSamp = (2**(mDR_MLBS_Order)-1)*mDR_OV
    tTimeStep = 1/(mDR_F0_Clk*mDR_OV) # equivalent sampling time step [ns]
    mDR_Ref_Times = np.arange(tNumSamp).T * tTimeStep # equivalent delay times [ns]

    tFrqStep = 1/(tTimeStep*tNumSamp)
    mDR_Ref_Frqs = np.fft.ifftshift(np.arange(np.ceil(-tNumSamp/2), np.ceil(tNumSamp/2)) * tFrqStep)

    # prepare ideal MLBS for correlation
    tNumSamp = 2**(mDR_MLBS_Order)-1
    tMLBSName = f"mlbs{mDR_MLBS_Order}.txt"
    dirName = os.path.dirname(os.path.abspath(__file__))
    tMLBSOrg = np.loadtxt(os.path.join(dirName, tMLBSName), delimiter=',').astype(np.double)
    tMLBSOrg = tMLBSOrg.reshape(-1, order='F')
    tMLBSOrg = tMLBSOrg[:tNumSamp]

    # construct reference MLBS
    tBB_MLBS = np.repeat(tMLBSOrg, mDR_OV)
    tF0_MLBS = tBB_MLBS * np.sin(2*np.pi*mDR_F0_Clk * mDR_Ref_Times)

    if mDR_OV > 1:
        mDR_Ref_MLBS = tBB_MLBS + tF0_MLBS # ideal baseband + up-mixed MLBS as reference signal
    else:
        mDR_Ref_MLBS = tBB_MLBS # ideal baseband MLBS as reference signal

    mDR_Ref_Spec = np.conj(np.exp(1j*np.angle(np.fft.fft(mDR_Ref_MLBS)))) # reference spectrum for correlation
    mDR_Ref_Spec[0] = 0 # exclude DC from reference since it cannot be measured reliably

    if mDR_OV > 1:
        # also suppress clock feed through due to unreliable DC
        mDR_Ref_Spec[tNumSamp+1] = mDR_Ref_Spec[tNumSamp+1] * 0.001
        mDR_Ref_Spec[(mDR_OV-1)*tNumSamp+1] = mDR_Ref_Spec[(mDR_OV-1)*tNumSamp+1] * 0.001

    return {
        "mDR_Ref_Spec": mDR_Ref_Spec,
        "mDR_Ref_MLBS": mDR_Ref_MLBS,
        "mDR_Ref_Times": mDR_Ref_Times,
        "mDR_Ref_Frqs": mDR_Ref_Frqs,
    }
