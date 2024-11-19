package org.jeongkkili.bombom.qualify.domain;

import org.hibernate.annotations.ColumnDefault;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Entity
@Table(name = "qualify_num")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class QualifyNum {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "qualify_num_id")
	private Long id;

	@Column(name = "qualify_number", unique = true, nullable = false)
	private String qualifyNumber;

	@Column(name = "in_use", nullable = false)
	@ColumnDefault("false")
	private Boolean inUse;

	@Builder
	public QualifyNum(String qualifyNumber) {
		this.qualifyNumber = qualifyNumber;
	}

	public void changeInUseTrue(Boolean inUse) {
		this.inUse = inUse;
	}
}
