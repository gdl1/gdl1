
#pragma once
#include "utils.h"
#include "ydlidar_driver.h"
#include <math.h>

#if !defined(__cplusplus)
#ifndef __cplusplus
#error "The YDLIDAR SDK requires a C++ compiler to be built"
#endif
#endif
#define PropertyBuilderByName(type, name, access_permission)\
    access_permission:\
        type m_##name;\
    public:\
    inline void set##name(type v) {\
        m_##name = v;\
    }\
    inline type get##name() {\
        return m_##name;\
}\

using namespace ydlidar;


class YDLIDAR_API CYdLidar
{
    PropertyBuilderByName(float,MaxRange,private)///< 최대 레이저 범위 설정 및 가져오기
    PropertyBuilderByName(float,MinRange,private)///< 최소 레이저 거리 측정 범위 설정 및 가져오기
    PropertyBuilderByName(float,MaxAngle,private)///< 레이저의 최대 각도를 설정하고 얻으십시오. 최대는 180도입니다.
    PropertyBuilderByName(float,MinAngle,private)///< 레이저의 최소 각도를 설정하고 얻으십시오. 최소값은 -180도입니다.
    PropertyBuilderByName(int,ScanFrequency,private)///< 레이저 스캐닝 주파수 설정 및 얻기(범위 5HZ~12HZ)

    PropertyBuilderByName(bool,Intensities,private)///< 레이저 벨트의 신호 품질 설정 및 가져오기(S4B 레이더에서만 지원됨)
    PropertyBuilderByName(bool,FixedResolution,private)///< 레이저가 고정 각도 해상도인지 설정 및 확인
    PropertyBuilderByName(bool,Exposure,private)///< S4 레이더에서만 지원되는 레이저를 설정하고 획득할 때 저조도 노출 모드를 켭니다.
    PropertyBuilderByName(bool,Reversion, private)///< 레이저를 180도 회전할지 여부를 설정하고 가져옵니다.
    PropertyBuilderByName(bool,AutoReconnect, private)///< 비정상 시 자동 재접속 여부 설정

    PropertyBuilderByName(int,SerialBaudrate,private)///< 레이저 통신의 전송 속도 설정 및 가져오기
    PropertyBuilderByName(int,SampleRate,private)///< 레이저 샘플링 주파수 설정 및 가져오기

    PropertyBuilderByName(std::string,SerialPort,private)///< 레이저 포트 번호 설정 및 가져오기
    PropertyBuilderByName(std::vector<float>,IgnoreArray,private)///< 레이저 제거 포인트 설정 및 획득


public:
	CYdLidar(); //!< Constructor
	virtual ~CYdLidar();  //!< Destructor: turns the laser off.

    bool initialize();  //!< Attempts to connect and turns the laser on. Raises an exception on error.

    // Return true if laser data acquistion succeeds, If it's not
    bool doProcessSimple(LaserScan &outscan, bool &hardwareError);

    //Turn on the motor enable
	bool  turnOn();  //!< See base class docs
    //Turn off the motor enable and close the scan
	bool  turnOff(); //!< See base class docs

    /** Returns true if the device is in good health, If it's not*/
	bool getDeviceHealth() const;

    /** Returns true if the device information is correct, If it's not*/
    bool getDeviceInfo(int &type);

    /** Retruns true if the scan frequency is set to user's frequency is successful, If it's not*/
    bool checkScanFrequency();

    //Turn off lidar connection
    void disconnecting(); //!< Closes the comms with the laser. Shouldn't have to be directly needed by the user

protected:
    /** Returns true if communication has been established with the device. If it's not,
      *  try to create a comms channel.
      * \return false on error.
      */
    bool  checkCOMMs();

    /** Returns true if health status and device information has been obtained with the device. If it's not,
      * \return false on error.
      */
    bool  checkStatus();

    /** Returns true if the normal scan runs with the device. If it's not,
      * \return false on error.
      */
    bool checkHardware();



private:
    bool isScanning;
    int node_counts ;
    double each_angle;
    bool m_isMultipleRate;
    double m_FrequencyOffset;

    YDlidarDriver *lidarPtr;
};	// End of class

